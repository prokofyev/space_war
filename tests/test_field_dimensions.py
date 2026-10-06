import pygame

from space_war.config import GameConfig
from space_war.game import world_from_display


def test_field_dimensions_follow_display():
    surface = pygame.Surface((640, 360))
    world = world_from_display(GameConfig(), surface)
    assert world.width == 640
    assert world.height == 360
    # Spawn positions scale with the field rather than using fixed pixels.
    assert 0 <= world.ships[0].position[0] <= 640
    assert 0 <= world.ships[1].position[1] <= 360
