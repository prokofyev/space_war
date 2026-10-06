"""Procedural sprite generation for ships, glows, and debris.

Everything here is presentational: it builds anti-aliased surfaces from the
configured colours. Nothing in this module affects the simulation.
"""
from __future__ import annotations

import math

import pygame

from .config import GameConfig

_SUPERSAMPLE = 4  # render at 4x and downscale for smooth edges


def _shade(color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    if factor >= 0.0:
        return tuple(min(255, int(c + (255 - c) * factor)) for c in color)
    return tuple(max(0, int(c * (1.0 + factor))) for c in color)


def _sprite_span(config: GameConfig) -> float:
    """Half-size of the sprite canvas so nose, fins, and glow all fit."""
    return config.ship_radius * 1.9 + config.flame_length * 0.2


def build_ship_surface(config: GameConfig, player: int) -> pygame.Surface:
    """Return an anti-aliased ship sprite with its nose pointing along +x."""
    base = config.ship_colors[player]
    radius = config.ship_radius
    span = _sprite_span(config)
    size = int(math.ceil(span * 2 * _SUPERSAMPLE))

    canvas = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = size / 2.0
    r = radius * _SUPERSAMPLE

    def point(dx: float, dy: float) -> tuple[float, float]:
        return (cx + dx * _SUPERSAMPLE, cy + dy * _SUPERSAMPLE)

    # Fins at the rear, splayed above and below the body.
    fin = _shade(base, -0.35)
    pygame.draw.polygon(
        canvas,
        fin,
        [point(-radius * 0.2, -radius * 0.75), point(-radius * 1.05, -radius * 0.95),
         point(-radius * 0.55, -radius * 0.15)],
    )
    pygame.draw.polygon(
        canvas,
        fin,
        [point(-radius * 0.2, radius * 0.75), point(-radius * 1.05, radius * 0.95),
         point(-radius * 0.55, radius * 0.15)],
    )

    # Exhaust nozzle.
    pygame.draw.rect(
        canvas,
        _shade(base, -0.5),
        pygame.Rect(
            int(cx - r * 1.05), int(cy - r * 0.4), int(r * 0.45), int(r * 0.8)
        ),
    )

    # Main torus body: outer disc, then a carved-out centre.
    pygame.draw.circle(canvas, base, (cx, cy), r)
    pygame.draw.circle(canvas, _shade(base, 0.25), (cx, cy - r * 0.22), r * 0.86, int(r * 0.32))
    hole = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(hole, (0, 0, 0, 0), (cx, cy), r * 0.5)
    canvas.blit(hole, (0, 0))

    # Nose accent so the facing direction is unmistakable.
    pygame.draw.polygon(
        canvas,
        _shade(base, 0.6),
        [point(radius * 0.55, -radius * 0.35), point(radius * 1.25, 0.0),
         point(radius * 0.55, radius * 0.35)],
    )

    # Cockpit accent.
    pygame.draw.circle(canvas, _shade(base, 0.75), point(radius * 0.15, 0.0), r * 0.28)

    small = pygame.transform.smoothscale(
        canvas, (int(math.ceil(span * 2)), int(math.ceil(span * 2)))
    )
    return small


def build_glow_surface(config: GameConfig, player: int) -> pygame.Surface:
    """Return a soft radial halo in the player's colour with per-pixel alpha."""
    base = config.ship_colors[player]
    extent = config.glow_radius * 1.6
    size = int(math.ceil(extent * 2))
    glow = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (size / 2.0, size / 2.0)
    for step in range(config.glow_steps, 0, -1):
        t = step / config.glow_steps
        radius = max(1, int(extent * t))
        alpha = int(70 * (1.0 - t) ** 2)
        pygame.draw.circle(glow, (*base, alpha), center, radius)
    return glow


class SpriteCache:
    """Pre-render and cache the per-player sprites so frames do not rebuild them."""

    def __init__(self, config: GameConfig) -> None:
        self.ship = [build_ship_surface(config, i) for i in (0, 1)]
        self.glow = [build_glow_surface(config, i) for i in (0, 1)]
