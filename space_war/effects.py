"""Render-layer visual effects: explosion debris and missile trails.

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

    def draw(self, surface: pygame.Surface, camera=None, viewport=None) -> None:
        for piece in self.pieces:
            t = piece.age / piece.lifetime if piece.lifetime > 0 else 1.0
            alpha = max(0, int(255 * (1.0 - t)))
            scale = camera.scale if camera is not None else 1.0
            if camera is not None and viewport is not None:
                position = camera.to_screen(piece.position, viewport)
            else:
                position = piece.position
            size = max(1, int(piece.size * (1.0 - 0.4 * t) * scale))
            chunk = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(chunk, (*piece.color, alpha), (size, size), size)
            surface.blit(chunk, (position[0] - size, position[1] - size))



def draw_missile_trail(
    surface: pygame.Surface,
    config: GameConfig,
    position: Vec,
    velocity: Vec,
    scale: float = 1.0,
) -> None:
    """Draw a fading trail behind a missile, opposite its velocity.

    ``position`` is already in screen space; ``scale`` is the camera zoom so
    the trail matches the missile's on-screen size.
    """
    speed = math.hypot(velocity[0], velocity[1])
    if speed == 0.0:
        return
    direction = (velocity[0] / speed, velocity[1] / speed)
    for i in range(config.trail_points, 0, -1):
        t = i / config.trail_points
        dist = config.trail_length * t * scale
        alpha = int(150 * (1.0 - t))
        size = max(1, int(config.missile_radius * (1.4 - t) * scale))
        point = (position[0] - direction[0] * dist, position[1] - direction[1] * dist)
        dot = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(dot, (255, 220, 150, alpha), (size, size), size)
        surface.blit(dot, (point[0] - size, point[1] - size))
