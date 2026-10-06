"""Draw a :class:`~space_war.world.World` onto a Pygame surface."""
from __future__ import annotations

import math

import pygame

from .world import World


def render(surface: pygame.Surface, world: World, font: pygame.font.Font) -> None:
    surface.fill(world.config.background)

    for index, missile in enumerate(world.missiles):
        color = world.config.missile_colors[missile.owner]
        radius = int(world.config.missile_radius)
        center = (int(missile.position[0]), int(missile.position[1]))
        pygame.draw.circle(surface, color, center, max(radius, 2))

    for index, ship in enumerate(world.ships):
        if not ship.alive:
            continue
        color = world.config.ship_colors[index]
        radius = world.config.ship_radius
        center = (int(ship.position[0]), int(ship.position[1]))
        # Draw the ship as a donut/torus: body circle with a hollow middle.
        pygame.draw.circle(surface, color, center, int(radius))
        pygame.draw.circle(surface, world.config.background, center, int(radius * 0.5))
        # Thrust direction marker.
        tip = (
            int(ship.position[0] + math.cos(ship.angle) * radius),
            int(ship.position[1] + math.sin(ship.angle) * radius),
        )
        pygame.draw.line(surface, (255, 255, 255), center, tip, 2)

    _draw_scores(surface, world, font)


def _draw_scores(surface: pygame.Surface, world: World, font: pygame.font.Font) -> None:
    for index, score in enumerate(world.scores):
        color = world.config.ship_colors[index]
        text = font.render(f"P{index + 1}: {score}   ammo {world.ammo[index]}", True, color)
        if index == 0:
            surface.blit(text, (24, 20))
        else:
            rect = text.get_rect(topright=(surface.get_width() - 24, 20))
            surface.blit(text, rect)
