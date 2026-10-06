import pygame

from space_war.config import GameConfig
from space_war.game import world_from_display
from space_war.render import render


def test_render_frame_runs_headless():
    surface = pygame.Surface((320, 240))
    world = world_from_display(GameConfig(), surface)
    font = pygame.font.SysFont("monospace", 16)
    # Draw several frames including a fired missile without raising.
    render(surface, world, font)
    from space_war.world import Controls

    world.step(0.016, [Controls(thrust=True), Controls(rotate=1)])
    world.step(0.016, [Controls(fire=True), Controls()])
    render(surface, world, font)
