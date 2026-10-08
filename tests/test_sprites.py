import pygame

from space_war import sprites
from space_war.config import GameConfig


def test_ship_sprite_is_nonempty_and_near_radius_times_scale():
    config = GameConfig()
    surface = sprites.build_ship_surface(config, 0)
    assert surface.get_flags() & pygame.SRCALPHA
    bounds = surface.get_bounding_rect()
    assert bounds.width > 0 and bounds.height > 0
    # The ship is drawn large enough to keep pace with its collision radius.
    assert surface.get_width() >= config.ship_radius
    assert surface.get_height() >= config.ship_radius


def test_ship_sprite_background_is_transparent():
    config = GameConfig()
    surface = sprites.build_ship_surface(config, 0)
    # Corners of the image background are keyed out (fully transparent).
    assert surface.get_at((0, 0)).a == 0
    assert surface.get_at((surface.get_width() - 1, 0)).a == 0


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
    assert len(cache.thrust) == 2
    assert len(cache.glow) == 2
    assert pygame.image.tostring(cache.ship[0], "RGBA") != pygame.image.tostring(
        cache.ship[1], "RGBA"
    )


def test_engine_variants_differ_per_player():
    config = GameConfig()
    for player in (0, 1):
        idle = sprites.build_ship_surface(config, player)
        thrusting = sprites.build_ship_surface(config, player, thrusting=True)
        assert pygame.image.tostring(idle, "RGBA") != pygame.image.tostring(
            thrusting, "RGBA"
        )


def test_rotating_sprite_changes_pixels():
    config = GameConfig()
    sprite = sprites.build_ship_surface(config, 0)
    a = pygame.transform.rotozoom(sprite, 0.0, 1.0)
    b = pygame.transform.rotozoom(sprite, -90.0, 1.0)
    assert pygame.image.tostring(a, "RGBA") != pygame.image.tostring(b, "RGBA")
