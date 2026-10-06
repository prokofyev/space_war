from space_war.entities import Missile
from space_war.world import Controls


def _kill(world, victim, winner):
    world.ships[victim].position = (50.0, 50.0)
    world.missiles.append(
        Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=winner)
    )
    world.step(1e-9, [Controls(), Controls()])


def test_surviving_player_scores_and_round_restarts(world):
    _kill(world, victim=1, winner=0)
    assert world.scores == [1, 0]
    # New round: both ships alive at start positions, no missiles.
    assert all(ship.alive for ship in world.ships)
    assert world.missiles == []
    assert world.ammo == [world.config.ammo_start, world.config.ammo_start]


def test_scores_accumulate_across_rounds(world):
    _kill(world, victim=1, winner=0)
    _kill(world, victim=0, winner=1)
    _kill(world, victim=1, winner=0)
    assert world.scores == [2, 1]


def test_destroyed_player_gets_no_point(world):
    _kill(world, victim=0, winner=1)
    assert world.scores == [0, 1]


def test_no_score_when_no_ship_destroyed(world):
    world.step(0.1, [Controls(), Controls()])
    assert world.scores == [0, 0]


def test_step_is_frame_rate_independent(world):
    # Same total elapsed time in one big step vs many small steps yields the
    # same position for a coasting ship.
    from space_war.world import World

    a = World(config=world.config, width=100.0, height=100.0)
    b = World(config=world.config, width=100.0, height=100.0)
    for w in (a, b):
        w.ships[0].position = (50.0, 50.0)
        w.ships[0].velocity = (20.0, 0.0)
        w.ships[1].position = (10.0, 10.0)
    a.step(0.5, [Controls(), Controls()])
    for _ in range(50):
        b.step(0.01, [Controls(), Controls()])
    assert abs(a.ships[0].position[0] - b.ships[0].position[0]) < 1e-6
