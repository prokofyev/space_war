import pygame

from space_war.config import GameConfig
from space_war.input import InputMapper


def _codes(config):
    return {
        p: {
            k: pygame.key.key_code(getattr(b, k))
            for k in ("rotate_ccw", "rotate_cw", "thrust", "fire")
        }
        for p, b in config.player_bindings.items()
    }


def test_held_fire_fires_once(fake_key):
    config = GameConfig()
    codes = _codes(config)
    mapper = InputMapper(config)
    fake_key([codes[1]["fire"]])
    first = mapper.poll()
    second = mapper.poll()
    assert first[0].fire is True
    assert second[0].fire is False


def test_bindings_map_to_correct_player(fake_key):
    config = GameConfig()
    codes = _codes(config)
    mapper = InputMapper(config)
    fake_key([codes[1]["thrust"], codes[2]["rotate_cw"]])
    controls = mapper.poll()
    assert controls[0].thrust is True
    assert controls[0].rotate == 0
    assert controls[1].rotate == 1
    assert controls[1].thrust is False


def test_rotation_directions(fake_key):
    config = GameConfig()
    codes = _codes(config)
    mapper = InputMapper(config)
    fake_key([codes[1]["rotate_ccw"], codes[2]["rotate_cw"]])
    controls = mapper.poll()
    assert controls[0].rotate == -1
    assert controls[1].rotate == 1
