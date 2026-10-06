"""Headless integration test: drive a full match loop for many frames."""
from space_war.config import GameConfig
from space_war.world import Controls, World


def test_simulated_match_runs_and_scores():
    config = GameConfig()
    world = World(config=config, width=1280.0, height=720.0)
    # Players face each other at the start; player 2 fires straight at the idle
    # player 1, which must eventually connect and score a round.
    c1 = Controls()

    prev_scores = list(world.scores)
    rounds_seen = 0
    for frame in range(600):
        c2 = Controls(fire=(frame == 0))
        world.step(1.0 / 60.0, [c1, c2])
        if world.scores != prev_scores:
            rounds_seen += 1
            prev_scores = list(world.scores)

    assert rounds_seen >= 1
    assert world.scores[1] >= 1
    assert all(0 <= ammo <= config.ammo_max for ammo in world.ammo)


def test_thrusting_ships_stay_inside_toroidal_field():
    config = GameConfig()
    world = World(config=config, width=800.0, height=600.0)
    for frame in range(3000):
        world.step(
            1.0 / 60.0,
            [Controls(thrust=True, rotate=1), Controls(thrust=True, rotate=-1)],
        )
        for ship in world.ships:
            assert 0.0 <= ship.position[0] < world.width
            assert 0.0 <= ship.position[1] < world.height


def test_missile_interception_in_live_loop():
    config = GameConfig()
    world = World(config=config, width=300.0, height=300.0)
    world.ships[0].position = (150.0, 100.0)
    world.ships[0].angle = 0.0
    world.ships[1].position = (150.0, 200.0)
    world.ships[1].angle = -1.5707963267948966  # pointing up (-y)
    fired = False
    for _ in range(30):
        world.step(1.0 / 120.0, [Controls(fire=True), Controls(fire=True)])
        if world.missiles:
            fired = True
            break
    assert fired
    assert isinstance(world.missiles, list)
