import math

from space_war.vector import length
from space_war.world import Controls, toroidal_delta


def _momentum(ships):
    return (ships[0].velocity[0] + ships[1].velocity[0],
            ships[0].velocity[1] + ships[1].velocity[1])


def _kinetic(ships):
    return 0.5 * (length(ships[0].velocity) ** 2 + length(ships[1].velocity) ** 2)


def test_head_on_collision_exchanges_velocities(world):
    a, b = world.ships
    a.position = (45.0, 50.0)
    b.position = (53.0, 50.0)  # within 2 * radius (10) so they overlap
    a.velocity = (20.0, 0.0)
    b.velocity = (-20.0, 0.0)
    world.step(0.0001, [Controls(), Controls()])
    assert math.isclose(a.velocity[0], -20.0, abs_tol=1e-6)
    assert math.isclose(b.velocity[0], 20.0, abs_tol=1e-6)


def test_glancing_collision_conserves_momentum_and_energy(world):
    a, b = world.ships
    a.position = (40.0, 40.0)
    b.position = (47.0, 43.0)
    a.velocity = (25.0, 5.0)
    b.velocity = (-10.0, 15.0)
    p0 = _momentum(world.ships)
    k0 = _kinetic(world.ships)
    world.step(0.0001, [Controls(), Controls()])
    p1 = _momentum(world.ships)
    k1 = _kinetic(world.ships)
    assert math.isclose(p0[0], p1[0], abs_tol=1e-6)
    assert math.isclose(p0[1], p1[1], abs_tol=1e-6)
    assert math.isclose(k0, k1, abs_tol=1e-6)


def test_collision_does_not_change_score(world):
    a, b = world.ships
    a.position = (40.0, 50.0)
    b.position = (45.0, 50.0)
    a.velocity = (10.0, 0.0)
    world.step(0.0001, [Controls(), Controls()])
    assert world.scores == [0, 0]
    assert a.alive and b.alive


def test_collision_separates_ships(world):
    a, b = world.ships
    a.position = (40.0, 50.0)
    b.position = (41.0, 50.0)
    world.step(0.0001, [Controls(), Controls()])
    dist = length(toroidal_delta(a.position, b.position, (world.width, world.height)))
    assert dist >= world.config.ship_radius * 2 - 1e-6


def test_toroidal_distance_across_seam(world):
    # Points near opposite edges are actually close on the torus.
    d = toroidal_delta((1.0, 50.0), (99.0, 50.0), (100.0, 100.0))
    assert length(d) == 2.0


def test_collision_detected_across_seam(world):
    a, b = world.ships
    a.position = (2.0, 50.0)
    b.position = (98.0, 50.0)  # distance 4 across the seam, radius sum 10
    a.velocity = (-5.0, 0.0)  # approaching across the seam
    b.velocity = (5.0, 0.0)
    world.step(0.0001, [Controls(), Controls()])
    # They collided: velocities reversed.
    assert a.velocity[0] > 0
    assert b.velocity[0] < 0
