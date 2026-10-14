"""Draw a :class:`~space_war.world.World` onto a Pygame surface.

The world is infinite, so drawing goes through a :class:`Camera` that keeps both
ships framed. The camera tracks the midpoint between the ships, picks a single
uniform scale that fits them on screen, and moves smoothly toward its target.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

from . import effects
from .sprites import SpriteCache
from .world import World


@dataclass
class Camera:
    """A uniform-zoom view of the infinite world, framing both ships."""

    center: tuple[float, float] = (0.0, 0.0)
    scale: float = 1.0
    initialized: bool = False

    def to_screen(
        self, position, viewport: tuple[int, int]
    ) -> tuple[float, float]:
        half_w = viewport[0] / 2.0
        half_h = viewport[1] / 2.0
        return (
            (position[0] - self.center[0]) * self.scale + half_w,
            (position[1] - self.center[1]) * self.scale + half_h,
        )

    def target(self, world: World, viewport: tuple[int, int]):
        """Return ``(center, scale)`` that frames both ships with a margin."""
        config = world.config
        a, b = world.ships[0].position, world.ships[1].position
        center = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
        # Use the drawn sprite extent so the whole image stays on screen.
        half = max(
            config.ship_radius,
            config.ship_radius * config.ship_sprite_scale / 2.0,
        )
        extent_x = abs(b[0] - a[0]) / 2.0 + half
        extent_y = abs(b[1] - a[1]) / 2.0 + half
        usable = 1.0 - config.camera_margin
        avail_x = viewport[0] / 2.0 * usable
        avail_y = viewport[1] / 2.0 * usable
        scale = min(avail_x / extent_x, avail_y / extent_y)
        return center, scale

    def follow(
        self, world: World, viewport: tuple[int, int], dt: float
    ) -> None:
        target_center, target_scale = self.target(world, viewport)
        if not self.initialized or dt <= 0.0:
            self.center = target_center
            self.scale = target_scale
            self.initialized = True
            return
        # Exponential smoothing, frame-rate independent and never overshooting.
        factor = 1.0 - math.exp(-world.config.camera_smoothing * dt)
        self.center = (
            self.center[0] + (target_center[0] - self.center[0]) * factor,
            self.center[1] + (target_center[1] - self.center[1]) * factor,
        )
        self.scale += (target_scale - self.scale) * factor


class Renderer:
    """Holds cached sprites and the visual effect state across frames."""

    def __init__(self, config) -> None:
        self.config = config
        self.sprites = SpriteCache(config)
        self.explosions = effects.ExplosionField(config)
        self.camera = Camera()
        self.elapsed = 0.0
        self._last_dt = 0.0
        self._in_pause = False

    def update(self, dt: float, world: World, controls) -> None:
        self.elapsed += dt
        self._last_dt = dt
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
        viewport = surface.get_size()
        self.camera.follow(world, viewport, self._last_dt)
        scale = self.camera.scale

        for missile in world.missiles:
            effects.draw_missile_trail(
                surface,
                self.config,
                self.camera.to_screen(missile.position, viewport),
                missile.velocity,
                scale,
            )
            color = self.config.missile_colors[missile.owner]
            radius = max(int(self.config.missile_radius * scale), 2)
            pygame.draw.circle(
                surface, color, self.camera.to_screen(missile.position, viewport), radius
            )

        for index, ship in enumerate(world.ships):
            if not ship.alive:
                continue
            self._draw_ship(surface, index, ship, controls, viewport, scale)

        self.explosions.draw(surface, self.camera, viewport)
        _draw_scores(surface, world, font)

    def _draw_ship(self, surface, index, ship, controls, viewport, scale) -> None:
        glow = self.sprites.glow[index]
        glow_scaled = _scaled(glow, scale)
        center = self.camera.to_screen(ship.position, viewport)
        surface.blit(
            glow_scaled,
            (center[0] - glow_scaled.get_width() / 2.0,
             center[1] - glow_scaled.get_height() / 2.0),
        )

        thrusting = bool(controls and index < len(controls) and controls[index].thrust)
        sprite = self.sprites.thrust[index] if thrusting else self.sprites.ship[index]
        rotated = pygame.transform.rotozoom(sprite, -math.degrees(ship.angle), scale)
        surface.blit(
            rotated,
            (center[0] - rotated.get_width() / 2.0,
             center[1] - rotated.get_height() / 2.0),
        )


def _scaled(surface: pygame.Surface, scale: float) -> pygame.Surface:
    if abs(scale - 1.0) < 1e-3:
        return surface
    size = (
        max(1, int(round(surface.get_width() * scale))),
        max(1, int(round(surface.get_height() * scale))),
    )
    return pygame.transform.smoothscale(surface, size)


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
