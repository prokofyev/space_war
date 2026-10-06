"""Fullscreen application entry point wiring input, simulation, and rendering."""
from __future__ import annotations

import pygame

from .config import GameConfig
from .input import InputMapper
from .render import Renderer
from .world import World

MAX_FRAME_DT = 0.05  # clamp huge deltas after stalls to keep physics stable


def world_from_display(config: GameConfig, surface: pygame.Surface) -> World:
    """Build a world whose field spans the given (fullscreen) surface."""
    return World(config=config, width=surface.get_width(), height=surface.get_height())


def run(config: GameConfig | None = None) -> None:
    config = config or GameConfig()
    pygame.init()
    try:
        surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Space War")
        world = world_from_display(config, surface)
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("monospace", 26)
        mapper = InputMapper(config)
        renderer = Renderer(config)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            dt = min(clock.tick(120) / 1000.0, MAX_FRAME_DT)
            controls = mapper.poll()
            world.step(dt, controls)
            renderer.update(dt, world, controls)
            renderer.draw(surface, world, font, controls)
            pygame.display.flip()
    finally:
        pygame.quit()
