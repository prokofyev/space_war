"""Tests for universal gravitational attraction between bodies."""
import math

import pytest
from dataclasses import replace

from space_war.config import GameConfig
from space_war.entities import Missile
from space_war.vector import length, sub
from space_war.world import Controls, World, euclidean_delta
from space_war import relativity


def _gravity_world(**overrides):
    config = replace(GameConfig(), thrust_accel=0.0, **overrides)
    return World(config=config)


def test_two_bodies_attract_each_other():
    world = _gravity_world()
    a, b = world.ships
    a.position = (400.0, 500.0)
    b.position = (600.0, 500.0)
    world._apply_gravity(1e-3)
    # a is pulled toward +x (toward b), b toward -x (toward a).
    assert a.velocity[0] > 0.0
    assert b.velocity[0] < 0.0


def test_attraction_magnitude_is_symmetric():
    world = _gravity_world()
    a, b = world.ships
    a.position = (400.0, 500.0)
    b.position = (600.0, 500.0)
    world._apply_gravity(1e-3)
    # Equal masses attract equally and oppositely.
    assert a.velocity[0] == pytest.approx(-b.velocity[0], rel=1e-12)


def test_force_falls_off_with_distance():
    near = _gravity_world()
    near.ships[0].position = (400.0, 500.0)
    near.ships[1].position = (500.0, 500.0)  # r = 100
    near._apply_gravity(1e-3)
    near_speed = abs(near.ships[0].velocity[0])

    far = _gravity_world()
    far.ships[0].position = (400.0, 500.0)
    far.ships[1].position = (600.0, 500.0)  # r = 200
    far._apply_gravity(1e-3)
    far_speed = abs(far.ships[0].velocity[0])

    # Doubling the distance quarters the force (inverse-square law).
    assert far_speed == pytest.approx(near_speed / 4.0, rel=1e-6)


def test_heavier_body_attracts_more():
    light = _gravity_world()
    light.ships[0].position = (400.0, 500.0)
    light.ships[1].position = (500.0, 500.0)
    light._apply_gravity(1e-3)
    light_force = abs(light.ships[1].velocity[0])

    heavy = _gravity_world(ship_mass=3.0)
    heavy.ships[0].position = (400.0, 500.0)
    heavy.ships[1].position = (500.0, 500.0)
    heavy._apply_gravity(1e-3)
    heavy_force = abs(heavy.ships[1].velocity[0])

    assert heavy_force == pytest.approx(3.0 * light_force, rel=1e-6)


def test_gravitational_constant_scales_force():
    weak = _gravity_world(gravitational_constant=1200.0)
    weak.ships[0].position = (400.0, 500.0)
    weak.ships[1].position = (500.0, 500.0)
    weak._apply_gravity(1e-3)

    strong = _gravity_world(gravitational_constant=3600.0)
    strong.ships[0].position = (400.0, 500.0)
    strong.ships[1].position = (500.0, 500.0)
    strong._apply_gravity(1e-3)

    assert strong.ships[0].velocity[0] == pytest.approx(
        3.0 * weak.ships[0].velocity[0], rel=1e-6
    )


def test_attraction_is_the_straight_line_between_bodies():
    world = _gravity_world()
    a, b = world.ships
    a.position = (20.0, 500.0)
    b.position = (60.0, 500.0)  # 40 px away, no wrap involved
    assert length(euclidean_delta(a.position, b.position)) == 40.0
    world._apply_gravity(1e-3)
    # a is pulled toward +x (toward b), b toward -x (toward a).
    assert a.velocity[0] > 0.0
    assert b.velocity[0] < 0.0


def test_coincident_bodies_stay_finite():
    world = _gravity_world()
    a, b = world.ships
    a.position = (500.0, 500.0)
    b.position = (500.0, 500.0)
    world._apply_gravity(1e-3)
    for ship in world.ships:
        assert math.isfinite(ship.velocity[0])
        assert math.isfinite(ship.velocity[1])


def test_near_coincident_bodies_stay_finite():
    world = _gravity_world()
    a, b = world.ships
    a.position = (500.0, 500.0)
    b.position = (500.0, 500.5)  # inside the softening radius
    world._apply_gravity(1e-3)
    for ship in world.ships:
        assert math.isfinite(ship.velocity[0])
        assert length(ship.velocity) < world.config.speed_of_light


def test_missiles_attract_and_are_attracted():
    world = _gravity_world()
    ship = world.ships[0]
    ship.position = (400.0, 500.0)
    # Park the other ship in the far corner; the nearby missile dominates.
    world.ships[1].position = (5.0, 5.0)
    world.missiles.append(
        Missile(position=(450.0, 500.0), velocity=(0.0, 0.0), owner=0)
    )
    world._apply_gravity(1e-3)
    missile = world.missiles[0]
    # Ship is pulled toward +x (toward the missile), missile toward -x.
    assert ship.velocity[0] > 0.0
    assert missile.velocity[0] < 0.0


def test_net_force_is_sum_of_pairwise_forces():
    world = _gravity_world()
    ship = world.ships[0]
    other = world.ships[1]
    ship.position = (400.0, 500.0)
    other.position = (600.0, 500.0)
    world.missiles.append(
        Missile(position=(400.0, 600.0), velocity=(0.0, 0.0), owner=1)
    )

    # Force magnitude helpers: F = G * m_i * m_j / r^2 along the unit direction.
    g = world.config.gravitational_constant
    m = world.config.ship_mass
    mm = world.config.missile_mass

    def pairwise(mass_i, mass_j, pos_i, pos_j):
        delta = euclidean_delta(pos_i, pos_j)
        r = length(delta)
        magnitude = g * mass_i * mass_j / (r * r)
        return (delta[0] / r * magnitude, delta[1] / r * magnitude)

    dt = 1e-3
    expected = pairwise(m, m, ship.position, other.position)
    f_missile = pairwise(m, mm, ship.position, world.missiles[0].position)
    expected = (expected[0] + f_missile[0], expected[1] + f_missile[1])

    world._apply_gravity(dt)
    # Gravity changes momentum by the net force times dt, and velocity follows
    # from that momentum relativistically. Comparing against the same exact
    # update keeps the check independent of the magnitude of G (a Newtonian
    # delta-v = F * dt / m approximation would only hold for weak gravity).
    c = world.config.speed_of_light
    p0 = relativity.momentum((0.0, 0.0), m, c)
    p_expected = (p0[0] + expected[0] * dt, p0[1] + expected[1] * dt)
    v_expected = relativity.velocity_from_momentum(p_expected, m, c)
    assert ship.velocity[0] == pytest.approx(v_expected[0], rel=1e-12)
    assert ship.velocity[1] == pytest.approx(v_expected[1], rel=1e-12)


def test_gravity_is_applied_by_step():
    world = _gravity_world()
    a, b = world.ships
    a.position = (400.0, 500.0)
    b.position = (600.0, 500.0)
    world.step(0.01, [Controls(), Controls()])
    assert a.velocity[0] > 0.0
    assert b.velocity[0] < 0.0


def test_gravity_acts_during_destruction_pause():
    world = _gravity_world()
    world.ships[1].position = (600.0, 500.0)
    world.missiles.append(
        Missile(position=(600.0, 500.0), velocity=(0.0, 0.0), owner=0)
    )
    world.step(1e-9, [Controls(), Controls()])
    assert not world.round_active  # the missile hit and started the pause
    survivor = world.ships[0]
    survivor.position = (400.0, 500.0)
    survivor.velocity = (0.0, 0.0)
    # A lingering missile gives the survivor a gravity partner during the pause.
    world.missiles.append(
        Missile(position=(500.0, 500.0), velocity=(0.0, 0.0), owner=1)
    )
    world.step(0.01, [Controls(), Controls()])
    # Even while no round is active, gravity keeps pulling bodies together.
    assert survivor.velocity[0] > 0.0


def test_gravity_never_exceeds_speed_of_light():
    world = _gravity_world(gravitational_constant=1e9)
    a, b = world.ships
    a.position = (500.0, 500.0)
    b.position = (500.0, 508.0)  # just at the softening floor
    for _ in range(200):
        world.step(0.02, [Controls(), Controls()])
    assert length(a.velocity) < world.config.speed_of_light
    assert length(b.velocity) < world.config.speed_of_light


def test_gravity_is_frame_rate_independent():
    a = _gravity_world()
    a.ships[0].position = (400.0, 500.0)
    a.ships[1].position = (600.0, 520.0)
    a.step(0.5, [Controls(), Controls()])

    b = _gravity_world()
    b.ships[0].position = (400.0, 500.0)
    b.ships[1].position = (600.0, 520.0)
    for _ in range(50):
        b.step(0.01, [Controls(), Controls()])

    assert a.ships[0].position[0] == pytest.approx(
        b.ships[0].position[0], rel=1e-4, abs=1e-3
    )
    assert a.ships[0].position[1] == pytest.approx(
        b.ships[0].position[1], rel=1e-4, abs=1e-3
    )
    assert a.ships[0].velocity[0] == pytest.approx(
        b.ships[0].velocity[0], rel=1e-3
    )
