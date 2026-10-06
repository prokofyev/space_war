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
