"""Ship and glow sprites loaded from the bundled ship artwork.

Ship sprites come from image files shipped inside the package: each player has
an "engines off" and an "engines on" image, the near-white image background is
cut out, and the result is scaled and pre-rotated so its nose points along +x.
All of this is presentational: nothing in this module affects the simulation.
"""
from __future__ import annotations

import math
from collections import deque
from pathlib import Path

import pygame

from .config import GameConfig

_ASSETS_DIR = Path(__file__).resolve().parent / "assets" / "ships"

# Per player: (engines off, engines on) file names. Player one is blue, two red.
_SHIP_FILES: tuple[tuple[str, str], tuple[str, str]] = (
    ("blue_engines_off.jpeg", "blue_engines_on.jpeg"),
    ("red_engines_off.jpeg", "red_engines_on.jpeg"),
)
_IMAGE_FACES_UP = -90.0  # degrees to rotate the nose-up artwork into +x

# The artwork sits on a near-white background. A pixel is treated as background
# when its darkest channel is this bright; the cut-out only removes background
# pixels connected to the image border, so bright highlights inside the ship
# (silver panels, the flame core) are kept.
_BACKGROUND_MIN_CHANNEL = 232
_BACKGROUND_WORK_SIZE = 256  # resolution the cut-out mask is computed at


def _sprite_size(config: GameConfig) -> int:
    """On-screen sprite length in pixels, tied to the ship's collision radius."""
    return max(2, int(round(config.ship_radius * config.ship_sprite_scale)))


def _remove_background(surface: pygame.Surface) -> pygame.Surface:
    """Return an SRCALPHA copy with the border-connected white background cleared."""
    work = _BACKGROUND_WORK_SIZE
    small = pygame.transform.smoothscale(surface, (work, work))
    near_white = [
        [min(small.get_at((x, y))[:3]) >= _BACKGROUND_MIN_CHANNEL for x in range(work)]
        for y in range(work)
    ]

    background = bytearray(work * work)
    queue: deque[tuple[int, int]] = deque()

    def visit(x: int, y: int) -> None:
        index = y * work + x
        if not background[index] and near_white[y][x]:
            background[index] = 1
            queue.append((x, y))

    for x in range(work):
        visit(x, 0)
        visit(x, work - 1)
    for y in range(work):
        visit(0, y)
        visit(work - 1, y)
    while queue:
        x, y = queue.popleft()
        if x > 0:
            visit(x - 1, y)
        if x < work - 1:
            visit(x + 1, y)
        if y > 0:
            visit(x, y - 1)
        if y < work - 1:
            visit(x, y + 1)

    cut = pygame.Surface((work, work), pygame.SRCALPHA)
    for y in range(work):
        row = y * work
        for x in range(work):
            red, green, blue, _ = small.get_at((x, y))
            alpha = 0 if background[row + x] else 255
            cut.set_at((x, y), (red, green, blue, alpha))
    return cut


def build_ship_surface(
    config: GameConfig, player: int, thrusting: bool = False
) -> pygame.Surface:
    """Return the player's ship sprite with its nose pointing along +x."""
    name = _SHIP_FILES[player][1 if thrusting else 0]
    cut = _remove_background(pygame.image.load(str(_ASSETS_DIR / name)))

    size = _sprite_size(config)
    scaled = pygame.transform.smoothscale(cut, (size, size))
    return pygame.transform.rotate(scaled, _IMAGE_FACES_UP)


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
        self.thrust = [build_ship_surface(config, i, thrusting=True) for i in (0, 1)]
        self.glow = [build_glow_surface(config, i) for i in (0, 1)]
