from space_war.config import GameConfig


def test_ships_share_equal_mass():
    config = GameConfig()
    assert config.ship_mass == config.ship_mass
    # A single mass value is used for both ships by the World.
    assert config.ship_mass > 0


def test_player_bindings_are_disjoint():
    config = GameConfig()
    p1 = config.player_bindings[1]
    p2 = config.player_bindings[2]
    keys1 = {p1.rotate_ccw, p1.rotate_cw, p1.thrust, p1.fire}
    keys2 = {p2.rotate_ccw, p2.rotate_cw, p2.thrust, p2.fire}
    assert len(keys1) == 4
    assert len(keys2) == 4
    assert keys1.isdisjoint(keys2)


def test_visual_and_timing_defaults_are_sane():
    config = GameConfig()
    assert config.destruction_pause > 0
    assert config.speed_of_light > 0
    for value in (
        config.debris_count,
        config.debris_speed,
        config.debris_min_speed,
        config.debris_lifetime,
        config.debris_size,
        config.flame_length,
        config.flame_width,
        config.flame_animation_speed,
        config.trail_length,
        config.trail_points,
        config.glow_radius,
        config.glow_steps,
    ):
        assert value > 0


def test_gravity_defaults_are_sane():
    config = GameConfig()
    assert config.gravitational_constant > 0
    assert config.missile_mass > 0
    assert config.missile_mass < config.ship_mass
    assert config.gravity_min_distance > 0
