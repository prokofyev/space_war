import pygame

from space_war.config import GameConfig
from space_war.game import world_from_display


def test_world_is_unbounded_and_independent_of_display():
    surface = pygame.Surface((640, 360))
    world = world_from_display(GameConfig(), surface)
    # The world has no dimensions and starts the ships from the configured
    # distance, not from the surface size.
    assert not hasattr(world, "width")
    assert not hasattr(world, "height")
    half = world.config.initial_ship_distance / 2.0
    assert world.ships[0].position == (-half, 0.0)
    assert world.ships[1].position == (half, 0.0)
