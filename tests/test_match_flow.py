from space_war.entities import Missile
from space_war.world import Controls


def _kill(world, victim, winner):
    world.ships[victim].position = (50.0, 50.0)
    world.missiles.append(
        Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=winner)
    )
    world.step(1e-9, [Controls(), Controls()])


def _finish_pause(world):
    """Advance past the destruction pause so the next round starts."""
    world.step(world.config.destruction_pause + 1e-6, [Controls(), Controls()])


def test_destruction_starts_pause_without_immediate_respawn(world):
    _kill(world, victim=1, winner=0)
    assert world.scores == [1, 0]
    # Score is awarded immediately, but the destroyed ship does not respawn yet.
    assert not world.round_active
    assert not world.ships[1].alive


def test_respawn_only_after_pause_elapses(world):
    _kill(world, victim=1, winner=0)
    world.step(world.config.destruction_pause * 0.5, [Controls(), Controls()])
    assert not world.ships[1].alive  # still paused
    _finish_pause(world)
    assert all(ship.alive for ship in world.ships)
    assert world.missiles == []
    assert world.ammo == [world.config.ammo_start, world.config.ammo_start]
    assert world.round_active


def test_no_scoring_during_pause(world):
    _kill(world, victim=1, winner=0)
    world.step(world.config.destruction_pause * 0.5, [Controls(), Controls()])
    assert world.scores == [1, 0]


def test_scores_accumulate_across_rounds(world):
    _kill(world, victim=1, winner=0)
    _finish_pause(world)
    _kill(world, victim=0, winner=1)
    _finish_pause(world)
    _kill(world, victim=1, winner=0)
    _finish_pause(world)
    assert world.scores == [2, 1]


def test_destroyed_player_gets_no_point(world):
    _kill(world, victim=0, winner=1)
    assert world.scores == [0, 1]


def test_no_score_when_no_ship_destroyed(world):
    world.step(0.1, [Controls(), Controls()])
    assert world.scores == [0, 0]


def test_pause_duration_is_configurable(world):
    from dataclasses import replace

    long_world = world.__class__(
        config=replace(world.config, destruction_pause=2.0), width=100.0, height=100.0
    )
    _kill(long_world, victim=1, winner=0)
    long_world.step(1.0, [Controls(), Controls()])
    assert not long_world.ships[1].alive  # 1.0s < 2.0s pause
    long_world.step(1.1, [Controls(), Controls()])
    assert long_world.ships[1].alive


def test_step_is_frame_rate_independent(world):
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


def test_world_keeps_moving_during_pause(world):
    survivor = world.ships[0]
    survivor.position = (20.0, 20.0)
    survivor.velocity = (30.0, 0.0)
    _kill(world, victim=1, winner=0)
    # Clear the survivor's own motion? No: keep momentum through the pause.
    before = survivor.position[0]
    world.step(world.config.destruction_pause * 0.4, [Controls(), Controls()])
    assert survivor.position[0] != before
    assert survivor.velocity == (30.0, 0.0)


def test_in_flight_missiles_move_during_pause(world):
    from space_war.entities import Missile

    _kill(world, victim=1, winner=0)
    world.missiles.append(
        Missile(position=(10.0, 10.0), velocity=(100.0, 0.0), owner=0, age=0.0)
    )
    world.step(world.config.destruction_pause * 0.3, [Controls(), Controls()])
    assert world.missiles
    assert world.missiles[0].position[0] > 10.0


def test_mutual_destruction_scores_both_and_closes_round(world):
    world.ships[0].position = (50.0, 50.0)
    world.ships[1].position = (60.0, 50.0)
    world.missiles.append(
        Missile(position=(60.0, 50.0), velocity=(0.0, 0.0), owner=0)
    )
    world.missiles.append(
        Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=1)
    )
    world.step(1e-9, [Controls(), Controls()])
    assert world.scores == [1, 1]
    assert not world.round_active
    assert not any(ship.alive for ship in world.ships)
    # The single window closes the round and respawns both ships.
    world.step(world.config.destruction_pause + 1e-6, [Controls(), Controls()])
    assert all(ship.alive for ship in world.ships)
    assert world.scores == [1, 1]


def test_gameplay_stays_active_during_round_end_window(world):
    # Destroy ship 1, leaving ship 0 alive inside the round-end window.
    world.ships[0].position = (10.0, 10.0)
    world.ships[1].position = (50.0, 50.0)
    _kill(world, victim=1, winner=0)
    assert not world.round_active
    assert world.scores == [1, 0]
    # Controls still move the survivor during the window.
    before = world.ships[0].position
    world.step(0.05, [Controls(thrust=True), Controls()])
    assert world.ships[0].position != before
    # A missile still in flight during the window destroys the survivor.
    world.ships[0].position = (50.0, 50.0)
    world.missiles.append(
        Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=1, armed=True)
    )
    world.step(1e-9, [Controls(), Controls()])
    assert not world.ships[0].alive
    assert world.scores == [1, 1]


def test_second_destruction_does_not_restart_window(world):
    world.ships[1].position = (50.0, 50.0)
    _kill(world, victim=1, winner=0)
    # Halfway through the window, kill the other ship too.
    world.step(world.config.destruction_pause * 0.5, [Controls(), Controls()])
    world.ships[0].position = (50.0, 50.0)
    world.missiles.append(
        Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=1, armed=True)
    )
    world.step(1e-9, [Controls(), Controls()])
    assert world.scores == [1, 1]
    assert not world.round_active
    # The timer was not reset: the round should close with the remaining half.
    world.step(world.config.destruction_pause * 0.5 + 1e-6, [Controls(), Controls()])
    assert all(ship.alive for ship in world.ships)


def test_no_further_scoring_after_window_elapses(world):
    # A dead ship is scored once and not again while it stays dead.
    world.ships[1].position = (50.0, 50.0)
    _kill(world, victim=1, winner=0)
    assert world.scores == [1, 0]
    for _ in range(5):
        world.step(world.config.destruction_pause * 0.1, [Controls(), Controls()])
    assert world.scores == [1, 0]
    assert not world.round_active


def test_ship_collision_death_scores_for_opponent(world):
    # Guard against regressions: any destruction awards the opponent, and both
    # dead in one round yields a point each.
    world.ships[1].position = (50.0, 50.0)
    world.missiles.append(
        Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=1, armed=True)
    )
    world.step(1e-9, [Controls(), Controls()])
    assert world.scores == [1, 0]  # self-destruction credits the opponent
