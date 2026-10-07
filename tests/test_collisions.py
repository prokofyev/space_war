import math

from space_war import relativity
from space_war.vector import length
from space_war.world import Controls, toroidal_delta


def _rel_momentum(ships, config):
    m0, c = config.ship_mass, config.speed_of_light
    pa = relativity.momentum(ships[0].velocity, m0, c)
    pb = relativity.momentum(ships[1].velocity, m0, c)
    return (pa[0] + pb[0], pa[1] + pb[1])


def _rel_energy(ships, config):
    m0, c = config.ship_mass, config.speed_of_light
    ea = relativity.energy(relativity.momentum(ships[0].velocity, m0, c), m0, c)
    eb = relativity.energy(relativity.momentum(ships[1].velocity, m0, c), m0, c)
    return ea + eb


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
    p0 = _rel_momentum(world.ships, world.config)
    e0 = _rel_energy(world.ships, world.config)
    world.step(0.0001, [Controls(), Controls()])
    p1 = _rel_momentum(world.ships, world.config)
    e1 = _rel_energy(world.ships, world.config)
    assert math.isclose(p0[0], p1[0], rel_tol=1e-9, abs_tol=1e-6)
    assert math.isclose(p0[1], p1[1], rel_tol=1e-9, abs_tol=1e-6)
    assert math.isclose(e0, e1, rel_tol=1e-9)
    # Neither ship may reach the speed of light.
    c = world.config.speed_of_light
    assert length(a.velocity) < c and length(b.velocity) < c


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
