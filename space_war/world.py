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
    round_active: bool = True

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
        self.round_active = True

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

        self._apply_controls(dt, controls)
        self._integrate_ships(dt)
        self._wrap_ships()
        self._resolve_ship_collisions()

        self._integrate_missiles(dt)
        self._wrap_missiles()
        self._expire_missiles()
        self._resolve_missile_ship_hits()
        self._resolve_missile_interceptions()

        self._resolve_round()

    def _apply_controls(self, dt: float, controls: list[Controls]) -> None:
        for i, ship in enumerate(self.ships):
            if not ship.alive:
                continue
            control = controls[i] if i < len(controls) else Controls()
            if control.rotate:
                ship.angle += control.rotate * self.config.rotation_speed * dt
            if control.thrust:
                acceleration = scale(from_angle(ship.angle), self.config.thrust_accel * dt)
                ship.velocity = add(ship.velocity, acceleration)
            if control.fire:
                self._fire(i)
            self._recharge_ammo(i, dt)

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
        if not self.round_active or self.ammo[index] <= 0:
            return
        ship = self.ships[index]
        muzzle = add(scale(from_angle(ship.angle), self.config.missile_speed), ship.velocity)
        self.missiles.append(
            Missile(position=ship.position, velocity=muzzle, owner=index, traveled=0.0)
        )
        self.ammo[index] -= 1

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
            missile.traveled += length(missile.velocity) * dt

    def _wrap_missiles(self) -> None:
        for missile in self.missiles:
            missile.position = self._wrap_position(missile.position)

    def _expire_missiles(self) -> None:
        self.missiles = [
            m for m in self.missiles if m.traveled < self.config.missile_range
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

        # Equal-mass elastic collision: exchange velocity components along the
        # collision normal (tangential components are preserved).
        if dot(sub(b.velocity, a.velocity), normal) < 0.0:
            a_normal = dot(a.velocity, normal)
            b_normal = dot(b.velocity, normal)
            a.velocity = add(a.velocity, scale(normal, b_normal - a_normal))
            b.velocity = add(b.velocity, scale(normal, a_normal - b_normal))

        # Separate overlapping ships along the normal.
        half = overlap / 2.0
        a.position = self._wrap_position(add(a.position, scale(normal, -half)))
        b.position = self._wrap_position(add(b.position, scale(normal, half)))

    def _resolve_missile_ship_hits(self) -> None:
        survivors: list[Missile] = []
        for missile in self.missiles:
            hit = False
            for i, ship in enumerate(self.ships):
                if i == missile.owner or not ship.alive:
                    continue
                if self.distance(missile.position, ship.position) <= (
                    self.config.missile_radius + self.config.ship_radius
                ):
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
                if mi.owner == mj.owner:
                    continue
                if self.distance(mi.position, mj.position) <= (
                    self.config.missile_radius * 2.0
                ):
                    removed.add(i)
                    removed.add(j)
        if removed:
            self.missiles = [m for k, m in enumerate(self.missiles) if k not in removed]

    def _resolve_round(self) -> None:
        dead = [i for i, ship in enumerate(self.ships) if not ship.alive]
        if len(dead) != 1:
            return
        winner = 1 - dead[0]
        self.scores[winner] += 1
        self.reset_round()
