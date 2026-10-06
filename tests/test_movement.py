import math

from dataclasses import replace

from space_war.world import Controls, World, wrap_scalar


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
    assert ship.velocity[0] == world.config.thrust_accel
    assert ship.velocity[1] == 0.0


def test_thrust_opposite_velocity_brakes(world):
    ship = world.ships[0]
    ship.velocity = (30.0, 0.0)
    ship.angle = math.pi
    world.step(1.0, _two_player_controls(Controls(thrust=True)))
    assert ship.velocity[0] == 30.0 - world.config.thrust_accel


def test_thrust_perpendicular_deflects(world):
    ship = world.ships[0]
    ship.velocity = (30.0, 0.0)
    ship.angle = -math.pi / 2  # facing up (negative y)
    world.step(1.0, _two_player_controls(Controls(thrust=True)))
    assert ship.velocity[0] == 30.0
    assert ship.velocity[1] == -world.config.thrust_accel


def test_wrap_scalar():
    assert wrap_scalar(-1.0, 100.0) == 99.0
    assert wrap_scalar(150.0, 100.0) == 50.0
    assert wrap_scalar(100.0, 100.0) == 0.0


def test_wrap_top_edge(world):
    ship = world.ships[0]
    ship.position = (40.0, -3.0)
    world._wrap_ships()
    assert ship.position == (40.0, 97.0)


def test_wrap_diagonal_corner(world):
    ship = world.ships[0]
    ship.velocity = (60.0, 60.0)
    ship.position = (95.0, 95.0)
    world.step(0.5, _two_player_controls())
    assert 0 <= ship.position[0] < world.width
    assert 0 <= ship.position[1] < world.height
    # Velocity and facing are preserved across the wrap.
    assert ship.velocity == (60.0, 60.0)


def test_wrap_preserves_velocity_and_facing(world):
    ship = world.ships[0]
    ship.velocity = (0.0, -80.0)
    ship.angle = 1.0
    ship.position = (10.0, 5.0)
    world.step(1.0, _two_player_controls())
    assert ship.position[1] < 50.0
    assert ship.velocity == (0.0, -80.0)
    assert ship.angle == 1.0
