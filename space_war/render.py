"""Draw a :class:`~space_war.world.World` onto a Pygame surface."""
from __future__ import annotations

import math

import pygame

from . import effects
from .sprites import SpriteCache
from .world import World


class Renderer:
    """Holds cached sprites and the visual effect state across frames."""

    def __init__(self, config) -> None:
        self.config = config
        self.sprites = SpriteCache(config)
        self.explosions = effects.ExplosionField(config)
        self.elapsed = 0.0
        self._in_pause = False

    def update(self, dt: float, world: World, controls) -> None:
        self.elapsed += dt
        # Clear debris when a new round begins (pause -> active transition).
        if not world.round_active:
            self._in_pause = True
        elif self._in_pause:
            self.explosions.clear()
            self._in_pause = False
        for index, position, angle, velocity in world.destroyed_events:
            self.explosions.spawn(position, self.config.ship_colors[index], velocity)
        self.explosions.update(dt)

    def draw(self, surface: pygame.Surface, world: World, font: pygame.font.Font,
             controls=None) -> None:
        surface.fill(self.config.background)

        for missile in world.missiles:
            effects.draw_missile_trail(
                surface, self.config, missile.position, missile.velocity
            )
            color = self.config.missile_colors[missile.owner]
            center = (int(missile.position[0]), int(missile.position[1]))
            pygame.draw.circle(surface, color, center, max(int(self.config.missile_radius), 2))

        for index, ship in enumerate(world.ships):
            if not ship.alive:
                continue
            self._draw_ship(surface, index, ship, controls)

        self.explosions.draw(surface)
        _draw_scores(surface, world, font)

    def _draw_ship(self, surface, index, ship, controls) -> None:
        glow = self.sprites.glow[index]
        surface.blit(
            glow,
            (ship.position[0] - glow.get_width() / 2.0,
             ship.position[1] - glow.get_height() / 2.0),
        )

        thrusting = bool(controls and index < len(controls) and controls[index].thrust)
        if thrusting:
            effects.draw_flame(
                surface, self.config, ship.position, ship.angle, self.elapsed
            )

        sprite = self.sprites.ship[index]
        rotated = pygame.transform.rotozoom(sprite, -math.degrees(ship.angle), 1.0)
        surface.blit(
            rotated,
            (ship.position[0] - rotated.get_width() / 2.0,
             ship.position[1] - rotated.get_height() / 2.0),
        )


def _draw_scores(surface: pygame.Surface, world: World, font: pygame.font.Font) -> None:
    for index, score in enumerate(world.scores):
        color = world.config.ship_colors[index]
        text = font.render(f"P{index + 1}: {score}   ammo {world.ammo[index]}", True, color)
        if index == 0:
            surface.blit(text, (24, 20))
        else:
            rect = text.get_rect(topright=(surface.get_width() - 24, 20))
            surface.blit(text, rect)


def render(surface: pygame.Surface, world: World, font: pygame.font.Font) -> None:
    """Backwards-compatible one-shot render used by tests; no persistent state."""
    Renderer(world.config).draw(surface, world, font)
