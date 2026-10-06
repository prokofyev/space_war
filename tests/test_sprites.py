import pygame

from space_war import sprites
from space_war.config import GameConfig


def test_ship_sprite_is_nonempty_and_larger_than_radius():
    config = GameConfig()
    surface = sprites.build_ship_surface(config, 0)
    assert surface.get_flags() & pygame.SRCALPHA
    bounds = surface.get_bounding_rect()
    assert bounds.width > 0 and bounds.height > 0
    assert bounds.width >= config.ship_radius and bounds.height >= config.ship_radius


def test_glow_surface_has_alpha():
    config = GameConfig()
    glow = sprites.build_glow_surface(config, 0)
    assert glow.get_flags() & pygame.SRCALPHA
    assert glow.get_bounding_rect().width > config.ship_radius


def test_player_sprites_differ_and_cache_builds_both():
    config = GameConfig()
    p0 = sprites.build_ship_surface(config, 0)
    p1 = sprites.build_ship_surface(config, 1)
    assert pygame.image.tostring(p0, "RGBA") != pygame.image.tostring(p1, "RGBA")

    cache = sprites.SpriteCache(config)
    assert len(cache.ship) == 2
    assert len(cache.glow) == 2
    assert pygame.image.tostring(cache.ship[0], "RGBA") != pygame.image.tostring(
        cache.ship[1], "RGBA"
    )
