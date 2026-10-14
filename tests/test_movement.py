import math

from dataclasses import replace

from space_war.world import Controls, World


def _two_player_controls(a=Controls(), b=Controls()):
    return [a, b]


def test_rotation_changes_angle_not_velocity(world):
    ship = world.ships[0]
    ship.velocity = (30.0, 0.0)
    world.step(1.0, _two_player_controls(Controls(rotate=1)))
    assert ship.angle == world.config.rotation_speed
    assert ship.velocity == (30.0, 0.0)


def test_rotate_counter_clockwise_decreases_angle(world):
    ship = world.ships[0]
    world.step(0.5, _two_player_controls(Controls(rotate=-1)))
    assert ship.angle == -world.config.rotation_speed * 0.5


def test_no_rotation_keeps_angle(world):
    ship = world.ships[0]
    ship.angle = 1.234
    world.step(1.0, _two_player_controls())
    assert ship.angle == 1.234


def test_coasting_preserves_velocity(world):
    ship = world.ships[0]
    ship.velocity = (40.0, 0.0)
    start = ship.position
    world.step(0.5, _two_player_controls())
    assert ship.velocity == (40.0, 0.0)
    assert ship.position[0] == start[0] + 20.0


def test_thrust_along_facing_accelerates(world):
    ship = world.ships[0]
    ship.angle = 0.0
    world.step(1.0, _two_player_controls(Controls(thrust=True)))
    # Low-speed (Newtonian) limit: ~ accel * dt, tiny relativistic correction.
    assert math.isclose(ship.velocity[0], world.config.thrust_accel, rel_tol=1e-4)
    assert ship.velocity[1] == 0.0


def test_thrust_opposite_velocity_brakes(world):
    ship = world.ships[0]
    ship.velocity = (30.0, 0.0)
    ship.angle = math.pi
    world.step(1.0, _two_player_controls(Controls(thrust=True)))
    assert math.isclose(
        ship.velocity[0], 30.0 - world.config.thrust_accel, rel_tol=1e-3
    )


def test_thrust_perpendicular_deflects(world):
    ship = world.ships[0]
    ship.velocity = (30.0, 0.0)
    ship.angle = -math.pi / 2  # facing up (negative y)
    world.step(1.0, _two_player_controls(Controls(thrust=True)))
    assert math.isclose(ship.velocity[0], 30.0, rel_tol=1e-3)
    assert math.isclose(ship.velocity[1], -world.config.thrust_accel, rel_tol=1e-3)


def test_ship_is_never_wrapped_by_an_edge(world):
    # The world is infinite: a ship far off-origin keeps its position offset,
    # velocity, and facing with no teleport to another part of the field.
    ship = world.ships[0]
    ship.velocity = (0.0, -80.0)
    ship.angle = 1.0
    ship.position = (10.0, 5.0)
    world.step(1.0, _two_player_controls())
    assert ship.position == (10.0, -75.0)
    assert ship.velocity == (0.0, -80.0)
    assert ship.angle == 1.0


def test_ships_fly_apart_without_bound(world):
    a, b = world.ships
    a.position = (0.0, 0.0)
    b.position = (100.0, 0.0)
    a.velocity = (-100.0, 0.0)
    b.velocity = (100.0, 0.0)
    world.step(1.0, _two_player_controls())
    assert a.position == (-100.0, 0.0)
    assert b.position == (200.0, 0.0)
    assert world.distance(a.position, b.position) == 300.0
