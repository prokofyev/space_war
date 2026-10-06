"""Render-layer visual effects: explosion debris, thrust flames, missile trails.

Nothing here is part of the simulation. Effects only read the world state and
draw onto a surface, so they never affect collision, damage, or scoring.
"""
from __future__ import annotations

import math
import random

import pygame

from .config import GameConfig
from .vector import Vec


class Debris:
    """A single explosion fragment."""

    __slots__ = ("position", "velocity", "age", "lifetime", "color", "size")

    def __init__(
        self,
        position: Vec,
        velocity: Vec,
        lifetime: float,
        color: tuple[int, int, int],
        size: float,
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.age = 0.0
        self.lifetime = lifetime
        self.color = color
        self.size = size


class ExplosionField:
    """Owns the debris produced by ship destruction events."""

    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.pieces: list[Debris] = []

    def clear(self) -> None:
        self.pieces = []

    def spawn(
        self,
        position: Vec,
        color: tuple[int, int, int],
        inherited_velocity: Vec = (0.0, 0.0),
    ) -> None:
        rng = random.Random(int(position[0]) * 73856093 ^ int(position[1]) * 19349663)
        for _ in range(self.config.debris_count):
            angle = rng.uniform(0.0, 2.0 * math.pi)
            speed = rng.uniform(self.config.debris_min_speed, self.config.debris_speed)
            velocity = (
                math.cos(angle) * speed + inherited_velocity[0],
                math.sin(angle) * speed + inherited_velocity[1],
            )
            self.pieces.append(
                Debris(
                    position=position,
                    velocity=velocity,
                    lifetime=self.config.debris_lifetime,
                    color=color,
                    size=self.config.debris_size,
                )
            )

    def update(self, dt: float) -> None:
        damping = max(0.0, 1.0 - self.config.debris_damping * dt)
        alive: list[Debris] = []
        for piece in self.pieces:
            piece.age += dt
            if piece.age >= piece.lifetime:
                continue
            piece.position = (
                piece.position[0] + piece.velocity[0] * dt,
                piece.position[1] + piece.velocity[1] * dt,
            )
            piece.velocity = (piece.velocity[0] * damping, piece.velocity[1] * damping)
            alive.append(piece)
        self.pieces = alive

    def draw(self, surface: pygame.Surface) -> None:
        for piece in self.pieces:
            t = piece.age / piece.lifetime if piece.lifetime > 0 else 1.0
            alpha = max(0, int(255 * (1.0 - t)))
            size = max(1, int(piece.size * (1.0 - 0.4 * t)))
            chunk = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(chunk, (*piece.color, alpha), (size, size), size)
            surface.blit(chunk, (piece.position[0] - size, piece.position[1] - size))


def draw_flame(
    surface: pygame.Surface,
    config: GameConfig,
    position: Vec,
    angle: float,
    elapsed: float,
) -> None:
    """Draw an animated thrust flame behind a ship's nozzle."""
    flicker = 0.65 + 0.35 * math.sin(elapsed * config.flame_animation_speed)
    length = config.flame_length * flicker
    half_width = config.flame_width / 2.0
    back = angle + math.pi

    def offset(dist: float, side: float) -> tuple[float, float]:
        ox = math.cos(back) * dist - math.sin(back) * side
        oy = math.sin(back) * dist + math.cos(back) * side
        return (position[0] + ox, position[1] + oy)

    base = config.ship_radius * 0.9
    flame = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.polygon(
        flame,
        (255, 190, 80, 220),
        [offset(base, -half_width), offset(base + length, 0.0), offset(base, half_width)],
    )
    pygame.draw.polygon(
        flame,
        (255, 240, 170, 230),
        [offset(base, -half_width * 0.5), offset(base + length * 0.6, 0.0),
         offset(base, half_width * 0.5)],
    )
    surface.blit(flame, (0, 0))


def draw_missile_trail(
    surface: pygame.Surface,
    config: GameConfig,
    position: Vec,
    velocity: Vec,
) -> None:
    """Draw a fading trail behind a missile, opposite its velocity."""
    speed = math.hypot(velocity[0], velocity[1])
    if speed == 0.0:
        return
    direction = (velocity[0] / speed, velocity[1] / speed)
    for i in range(config.trail_points, 0, -1):
        t = i / config.trail_points
        dist = config.trail_length * t
        alpha = int(150 * (1.0 - t))
        size = max(1, int(config.missile_radius * (1.4 - t)))
        point = (position[0] - direction[0] * dist, position[1] - direction[1] * dist)
        dot = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(dot, (255, 220, 150, alpha), (size, size), size)
        surface.blit(dot, (point[0] - size, point[1] - size))
