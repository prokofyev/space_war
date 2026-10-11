"""Deterministic, window-free simulation of a two-player match.

``World`` owns all mutable state (ships, missiles, ammo, scores) and advances
it through :meth:`World.step`. It only depends on :mod:`space_war.config`,
:mod:`space_war.entities`, and :mod:`space_war.vector`, so it can be tested
headlessly without a display.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .config import GameConfig
from .entities import Missile, Ship
from . import relativity
from .vector import Vec, add, dot, from_angle, length, normalize, scale, sub


@dataclass
class Controls:
    """A single player's intent for one frame."""

    thrust: bool = False
    rotate: int = 0          # -1 counter-clockwise, +1 clockwise, 0 none
    fire: bool = False


def wrap_scalar(value: float, size: float) -> float:
    """Wrap a single coordinate into ``[0, size)``."""
    return value % size


def toroidal_delta(a: Vec, b: Vec, size: Vec) -> Vec:
    """Shortest vector from ``a`` to ``b`` on a torus of the given size."""
    dx = (b[0] - a[0]) % size[0]
    dy = (b[1] - a[1]) % size[1]
    if dx > size[0] / 2.0:
        dx -= size[0]
    if dy > size[1] / 2.0:
        dy -= size[1]
    return (dx, dy)


# Gravity is sub-stepped so a single large frame produces the same result as
# many small frames, and close encounters stay stable.
_MAX_GRAVITY_SUBSTEP = 1.0 / 240.0


@dataclass
class World:
    config: GameConfig
    width: float
    height: float
    ships: list[Ship] = field(default_factory=list)
    missiles: list[Missile] = field(default_factory=list)
    scores: list[int] = field(default_factory=lambda: [0, 0])
    ammo: list[int] = field(default_factory=list)
    recharge: list[float] = field(default_factory=lambda: [0.0, 0.0])
    cooldowns: list[float] = field(default_factory=lambda: [0.0, 0.0])
    round_scored: list[bool] = field(default_factory=lambda: [False, False])
    round_active: bool = True
    round_pause_remaining: float = 0.0
    destroyed_events: list[tuple[int, Vec, float, Vec]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.reset_round()

    # -- setup ---------------------------------------------------------------
    def reset_round(self) -> None:
        self.ships = []
        for i in range(2):
            fx, fy = self.config.start_positions[i]
            self.ships.append(
                Ship(
                    position=(fx * self.width, fy * self.height),
                    velocity=(0.0, 0.0),
                    angle=self.config.start_facings[i],
                    alive=True,
                )
            )
        self.missiles = []
        self.ammo = [self.config.ammo_start, self.config.ammo_start]
        self.recharge = [0.0, 0.0]
        self.cooldowns = [0.0, 0.0]
        self.round_scored = [False, False]
        self.round_active = True
        self.round_pause_remaining = 0.0

    # -- helpers -------------------------------------------------------------
    @property
    def _size(self) -> Vec:
        return (self.width, self.height)

    def ship_radius(self) -> float:
        return self.config.ship_radius

    def missile_radius(self) -> float:
        return self.config.missile_radius

    def _wrap_position(self, position: Vec) -> Vec:
        return (wrap_scalar(position[0], self.width), wrap_scalar(position[1], self.height))

    def distance(self, a: Vec, b: Vec) -> float:
        return length(toroidal_delta(a, b, self._size))

    # -- main step -----------------------------------------------------------
    def step(self, dt: float, controls: list[Controls]) -> None:
        if dt <= 0:
            return

        self.destroyed_events = []

        # The round-end window is not a freeze: controls, firing, movement,
        # gravity, wrapping, expiry, and missile damage all keep running. Only
        # the respawn waits for the window to elapse, and the window timer is
        # started once, at the first destruction, never restarted.
        self._apply_controls(dt, controls)
        self._advance_bodies(dt)
        self._wrap_ships()
        self._wrap_missiles()
        self._resolve_ship_collisions()
        self._expire_missiles()
        self._resolve_missile_ship_hits()
        self._resolve_missile_interceptions()

        self._resolve_round()

        if not self.round_active:
            self.round_pause_remaining -= dt
            if self.round_pause_remaining <= 0.0:
                self.reset_round()

    def _apply_controls(self, dt: float, controls: list[Controls]) -> None:
        for i in range(len(self.cooldowns)):
            self.cooldowns[i] = max(0.0, self.cooldowns[i] - dt)
        for i, ship in enumerate(self.ships):
            if not ship.alive:
                continue
            control = controls[i] if i < len(controls) else Controls()
            if control.rotate:
                ship.angle += control.rotate * self.config.rotation_speed * dt
            if control.thrust:
                self._thrust(ship, dt)
            if control.fire:
                self._fire(i)
            self._recharge_ammo(i, dt)

    def _thrust(self, ship: Ship, dt: float) -> None:
        """Apply thrust as a force over time: ``p += F * dt`` along the facing."""
        config = self.config
        force = config.thrust_accel * config.ship_mass
        p = relativity.momentum(ship.velocity, config.ship_mass, config.speed_of_light)
        p = add(p, scale(from_angle(ship.angle), force * dt))
        ship.velocity = relativity.velocity_from_momentum(
            p, config.ship_mass, config.speed_of_light
        )

    def _recharge_ammo(self, index: int, dt: float) -> None:
        if self.ammo[index] >= self.config.ammo_max:
            self.recharge[index] = 0.0
            return
        self.recharge[index] += dt
        while (
            self.recharge[index] >= self.config.ammo_replenish_interval
            and self.ammo[index] < self.config.ammo_max
        ):
            self.recharge[index] -= self.config.ammo_replenish_interval
            self.ammo[index] += 1

    def _fire(self, index: int) -> None:
        if self.ammo[index] <= 0 or self.cooldowns[index] > 0.0:
            return
        ship = self.ships[index]
        muzzle_local = scale(from_angle(ship.angle), self.config.missile_speed)
        muzzle = relativity.add_velocities(
            muzzle_local, ship.velocity, self.config.speed_of_light
        )
        self.missiles.append(
            Missile(position=ship.position, velocity=muzzle, owner=index, age=0.0)
        )
        self.ammo[index] -= 1
        self.cooldowns[index] = self.config.fire_cooldown

    def _advance_bodies(self, dt: float) -> None:
        """Apply gravity and move every body, sub-stepped for stability."""
        if self.config.gravitational_constant == 0.0:
            self._integrate_ships(dt)
            self._integrate_missiles(dt)
            return
        substeps = max(1, math.ceil(dt / _MAX_GRAVITY_SUBSTEP))
        sub_dt = dt / substeps
        for _ in range(substeps):
            self._apply_gravity(sub_dt)
            self._integrate_ships(sub_dt)
            self._integrate_missiles(sub_dt)

    def _apply_gravity(self, dt: float) -> None:
        """Pull every body toward every other with an inverse-square force.

        Ships and missiles are both sources and targets. Distances are the
        shortest toroidal separation, so attraction works across the edges.
        Each force is applied as a momentum change (``p += F * dt``) and the
        velocity is recovered from momentum, so gravity can never push a body to
        the speed of light. The distance is clamped by ``gravity_min_distance``
        so coincident bodies stay finite (their direction is undefined, so such
        a pair contributes no force).
        """
        config = self.config
        if config.gravitational_constant == 0.0:
            return
        bodies: list[tuple[Ship | Missile, float]] = []
        for ship in self.ships:
            if ship.alive:
                bodies.append((ship, config.ship_mass))
        for missile in self.missiles:
            bodies.append((missile, config.missile_mass))
        if len(bodies) < 2:
            return

        size = self._size
        g = config.gravitational_constant
        r_min = config.gravity_min_distance
        net: list[Vec] = [(0.0, 0.0)] * len(bodies)

        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                delta = toroidal_delta(
                    bodies[i][0].position, bodies[j][0].position, size
                )
                r = length(delta)
                if r == 0.0:
                    continue
                r_eff = max(r, r_min)
                magnitude = g * bodies[i][1] * bodies[j][1] / (r_eff * r_eff)
                direction = scale(delta, 1.0 / r)
                force = scale(direction, magnitude)
                net[i] = add(net[i], force)
                net[j] = sub(net[j], force)

        c = config.speed_of_light
        for k, (body, mass) in enumerate(bodies):
            p = relativity.momentum(body.velocity, mass, c)
            p = add(p, scale(net[k], dt))
            body.velocity = relativity.velocity_from_momentum(p, mass, c)

    def _integrate_ships(self, dt: float) -> None:
        for ship in self.ships:
            if not ship.alive:
                continue
            ship.position = add(ship.position, scale(ship.velocity, dt))

    def _wrap_ships(self) -> None:
        for ship in self.ships:
            ship.position = self._wrap_position(ship.position)

    def _integrate_missiles(self, dt: float) -> None:
        for missile in self.missiles:
            missile.position = add(missile.position, scale(missile.velocity, dt))
            missile.age += dt

    def _wrap_missiles(self) -> None:
        for missile in self.missiles:
            missile.position = self._wrap_position(missile.position)

    def _expire_missiles(self) -> None:
        self.missiles = [
            m for m in self.missiles if m.age < self.config.missile_lifetime
        ]

    def _resolve_ship_collisions(self) -> None:
        radius = self.config.ship_radius
        a, b = self.ships
        if not (a.alive and b.alive):
            return
        delta = toroidal_delta(a.position, b.position, self._size)
        dist = length(delta)
        min_dist = radius * 2.0
        if dist >= min_dist or dist == 0.0:
            if dist == 0.0:
                normal = (1.0, 0.0)
                overlap = min_dist
            else:
                return
        else:
            overlap = min_dist - dist
            normal = normalize(delta)

        # Relativistic elastic collision of two equal rest-mass bodies: resolve
        # in the center-of-momentum frame, where each body simply reverses its
        # momentum, then boost back. At low speed this reduces to the Newtonian
        # velocity exchange and it can never push a ship to the speed of light.
        if dot(sub(b.velocity, a.velocity), normal) < 0.0:
            self._elastic_collide(a, b)

        # Separate overlapping ships along the normal.
        half = overlap / 2.0
        a.position = self._wrap_position(add(a.position, scale(normal, -half)))
        b.position = self._wrap_position(add(b.position, scale(normal, half)))

    def _elastic_collide(self, a: Ship, b: Ship) -> None:
        config = self.config
        c = config.speed_of_light
        m0 = config.ship_mass
        pa = relativity.momentum(a.velocity, m0, c)
        pb = relativity.momentum(b.velocity, m0, c)
        ea = relativity.energy(pa, m0, c)
        eb = relativity.energy(pb, m0, c)

        p_total = add(pa, pb)
        e_total = ea + eb
        frame = scale(p_total, c * c / e_total)

        pa_com, _ = relativity.boost(pa, ea, frame, c)
        pb_com, _ = relativity.boost(pb, eb, frame, c)
        pa_com = scale(pa_com, -1.0)
        pb_com = scale(pb_com, -1.0)
        ea_com, eb_com = relativity.energy(pa_com, m0, c), relativity.energy(pb_com, m0, c)
        pa_out, _ = relativity.boost(pa_com, ea_com, scale(frame, -1.0), c)
        pb_out, _ = relativity.boost(pb_com, eb_com, scale(frame, -1.0), c)

        a.velocity = relativity.velocity_from_momentum(pa_out, m0, c)
        b.velocity = relativity.velocity_from_momentum(pb_out, m0, c)

    def _resolve_missile_ship_hits(self) -> None:
        survivors: list[Missile] = []
        for missile in self.missiles:
            hit = False
            owner_ship = self.ships[missile.owner]
            hit_radius = self.config.missile_radius + self.config.ship_radius
            if not missile.armed:
                if self.distance(missile.position, owner_ship.position) > hit_radius:
                    missile.armed = True
            for i, ship in enumerate(self.ships):
                if not ship.alive:
                    continue
                if i == missile.owner and not missile.armed:
                    continue
                if self.distance(missile.position, ship.position) <= hit_radius:
                    ship.alive = False
                    hit = True
                    break
            if not hit:
                survivors.append(missile)
        self.missiles = survivors

    def _resolve_missile_interceptions(self) -> None:
        removed: set[int] = set()
        count = len(self.missiles)
        for i in range(count):
            for j in range(i + 1, count):
                if i in removed or j in removed:
                    continue
                mi = self.missiles[i]
                mj = self.missiles[j]
                if self.distance(mi.position, mj.position) <= (
                    self.config.missile_radius * 2.0
                ):
                    removed.add(i)
                    removed.add(j)
        if removed:
            self.missiles = [m for k, m in enumerate(self.missiles) if k not in removed]

    def _resolve_round(self) -> None:
        for i, ship in enumerate(self.ships):
            if ship.alive or self.round_scored[i]:
                continue
            self.round_scored[i] = True
            self.scores[1 - i] += 1
            self.destroyed_events.append(
                (i, ship.position, ship.angle, ship.velocity)
            )
            if self.round_active:
                self.round_active = False
                self.round_pause_remaining = self.config.destruction_pause
