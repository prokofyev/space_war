import math

import pytest
from dataclasses import replace

from space_war import relativity
from space_war.config import GameConfig
from space_war.vector import length
from space_war.world import Controls, World


def _world(config, width=1000.0, height=1000.0):
    return World(config=config, width=width, height=height)


def test_gamma_grows_with_speed():
    c = 100.0
    assert relativity.gamma(0.0, c) == pytest.approx(1.0)
    assert relativity.gamma(50.0, c) == pytest.approx(1.0 / math.sqrt(1 - 0.25))
    assert relativity.gamma(99.0, c) > relativity.gamma(50.0, c)


def test_momentum_velocity_roundtrip():
    c = 1000.0
    m0 = 2.0
    for speed in (0.0, 1.0, 50.0, 300.0, 900.0, 999.0):
        v = (speed, 0.0)
        p = relativity.momentum(v, m0, c)
        back = relativity.velocity_from_momentum(p, m0, c)
        assert back[0] == pytest.approx(speed, rel=1e-9, abs=1e-6)
        assert back[1] == pytest.approx(0.0, abs=1e-9)


def test_velocity_from_momentum_never_reaches_c():
    c = 1000.0
    p = (1e12, 0.0)  # absurd momentum
    v = relativity.velocity_from_momentum(p, 1.0, c)
    assert length(v) < c


def test_gamma_does_not_produce_nan_near_c():
    val = relativity.gamma(1000.0, 1000.0)  # at/over c
    assert math.isfinite(val)


def test_thrust_approaches_c_but_never_reaches():
    config = replace(GameConfig(), speed_of_light=1000.0, thrust_accel=500.0)
    world = _world(config)
    ship = world.ships[0]
    ship.angle = 0.0
    for _ in range(20000):
        world.step(0.02, [Controls(thrust=True), Controls()])
    assert length(ship.velocity) < config.speed_of_light
    assert length(ship.velocity) > 0.5 * config.speed_of_light


def test_acceleration_diminishes_near_c():
    config = replace(GameConfig(), speed_of_light=1000.0, thrust_accel=100.0)
    low = _world(config)
    low.ships[0].angle = 0.0
    low.step(0.05, [Controls(thrust=True), Controls()])
    low_gain = length(low.ships[0].velocity)

    high = _world(config)
    high.ships[0].angle = 0.0
    high.ships[0].velocity = (995.0, 0.0)
    high.step(0.05, [Controls(thrust=True), Controls()])
    high_gain = length(high.ships[0].velocity) - 995.0

    assert high_gain < low_gain


def test_braking_still_works_near_c():
    config = replace(GameConfig(), speed_of_light=1000.0, thrust_accel=100.0)
    world = _world(config)
    ship = world.ships[0]
    ship.velocity = (900.0, 0.0)
    ship.angle = math.pi
    world.step(0.1, [Controls(thrust=True), Controls()])
    assert length(ship.velocity) < 900.0


def test_perpendicular_thrust_deflects_near_c():
    config = replace(GameConfig(), speed_of_light=1000.0, thrust_accel=100.0)
    world = _world(config)
    ship = world.ships[0]
    ship.velocity = (900.0, 0.0)
    ship.angle = -math.pi / 2
    world.step(0.1, [Controls(thrust=True), Controls()])
    assert ship.velocity[1] < 0.0
    assert length(ship.velocity) < config.speed_of_light


def test_thrust_is_frame_rate_independent():
    config = replace(GameConfig(), speed_of_light=1000.0, thrust_accel=200.0)

    a = _world(config)
    a.ships[0].angle = 0.0
    a.ships[1].position = (10.0, 10.0)
    a.step(1.0, [Controls(thrust=True), Controls()])

    b = _world(config)
    b.ships[0].angle = 0.0
    b.ships[1].position = (10.0, 10.0)
    for _ in range(100):
        b.step(0.01, [Controls(thrust=True), Controls()])

    assert length(a.ships[0].velocity) == pytest.approx(
        length(b.ships[0].velocity), rel=1e-3
    )


def test_missile_from_fast_ship_stays_below_c():
    config = replace(
        GameConfig(), speed_of_light=1000.0, missile_speed=200.0, thrust_accel=0.0
    )
    world = _world(config)
    ship = world.ships[0]
    ship.angle = 0.0
    ship.velocity = (995.0, 0.0)  # near c
    world.step(1e-9, [Controls(fire=True), Controls()])
    missile = world.missiles[0]
    assert length(missile.velocity) < config.speed_of_light


def test_missile_launch_matches_naive_sum_at_low_speed():
    config = replace(
        GameConfig(), speed_of_light=2000.0, missile_speed=50.0, thrust_accel=0.0
    )
    world = _world(config)
    ship = world.ships[0]
    ship.angle = 0.0
    ship.velocity = (30.0, 5.0)
    world.step(1e-9, [Controls(fire=True), Controls()])
    missile = world.missiles[0]
    # Low-speed limit of relativistic addition ~ naive sum (small SR correction).
    assert missile.velocity[0] == pytest.approx(80.0, rel=1e-3)
    assert missile.velocity[1] == pytest.approx(5.0, rel=1e-3)


def test_missile_in_flight_never_exceeds_c():
    config = replace(GameConfig(), speed_of_light=1000.0)
    world = _world(config)
    from space_war.entities import Missile

    world.missiles.append(
        Missile(position=(10.0, 10.0), velocity=(999.0, 0.0), owner=0, traveled=0.0)
    )
    for _ in range(50):
        world.step(0.016, [Controls(), Controls()])
    for missile in world.missiles:
        assert length(missile.velocity) < config.speed_of_light


def test_fast_collision_keeps_both_below_c():
    config = replace(GameConfig(), speed_of_light=1000.0, ship_radius=5.0)
    world = _world(config, width=200.0, height=200.0)
    a, b = world.ships
    a.position = (95.0, 100.0)
    b.position = (104.0, 100.0)
    a.velocity = (999.0, 0.0)
    b.velocity = (-999.0, 0.0)
    world.step(1e-9, [Controls(), Controls()])
    assert length(a.velocity) < config.speed_of_light
    assert length(b.velocity) < config.speed_of_light


def test_low_speed_collision_matches_newtonian():
    config = replace(GameConfig(), speed_of_light=2000.0, ship_radius=5.0)
    world = _world(config, width=200.0, height=200.0)
    a, b = world.ships
    a.position = (95.0, 100.0)
    b.position = (104.0, 100.0)
    a.velocity = (20.0, 0.0)
    b.velocity = (-20.0, 0.0)
    world.step(1e-9, [Controls(), Controls()])
    # Newtonian equal-mass head-on: velocities exchange ~ signs flip.
    assert a.velocity[0] == pytest.approx(-20.0, rel=1e-3)
    assert b.velocity[0] == pytest.approx(20.0, rel=1e-3)
