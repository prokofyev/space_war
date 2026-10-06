"""Central configuration for Space War.

Tunable gameplay constants and per-player keyboard bindings live here so that
the simulation modules never read module-level globals: they receive a
``GameConfig`` instance, which lets tests build tiny worlds via
``dataclasses.replace`` without touching the rules.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass(frozen=True)
class PlayerBindings:
    """Keyboard bindings for a single player, given as portable key names."""

    rotate_ccw: str
    rotate_cw: str
    thrust: str
    fire: str


@dataclass(frozen=True)
class GameConfig:
    """All tunable gameplay values.

    Field dimensions are intentionally absent: they come from the fullscreen
    display resolution at runtime and are passed to :class:`World`.
    """

    # Ship physics
    ship_radius: float = 16.0
    ship_mass: float = 1.0
    rotation_speed: float = 3.4          # radians / second
    thrust_accel: float = 320.0          # pixels / second^2

    # Missiles
    missile_speed: float = 620.0         # pixels / second added along facing
    missile_radius: float = 4.0
    missile_range: float = 900.0         # pixels flown before self-destruct

    # Ammunition
    ammo_start: int = 3
    ammo_max: int = 3
    ammo_replenish_interval: float = 3.0  # seconds per replenished missile

    # Round timing
    destruction_pause: float = 1.0       # seconds between destruction and respawn

    # Presentation: explosion and effects
    debris_count: int = 14
    debris_speed: float = 170.0          # pixels / second, initial outward speed
    debris_min_speed: float = 60.0
    debris_lifetime: float = 0.9         # seconds before a piece disappears
    debris_size: float = 3.5             # pixels
    debris_damping: float = 2.0          # velocity decay per second
    flame_length: float = 26.0           # pixels at full flicker
    flame_width: float = 12.0            # pixels across the nozzle
    flame_animation_speed: float = 20.0  # flicker rate
    trail_length: float = 26.0           # pixels of missile trail
    trail_points: int = 6
    glow_radius: float = 22.0            # pixels of halo around a ship
    glow_steps: int = 18

    # Spawn: positions as fractions of (width, height), facings in radians
    start_positions: tuple[tuple[float, float], tuple[float, float]] = (
        (0.25, 0.5),
        (0.75, 0.5),
    )
    start_facings: tuple[float, float] = (0.0, math.pi)

    # Per-player bindings
    player_bindings: dict[int, PlayerBindings] = field(
        default_factory=lambda: {
            1: PlayerBindings("a", "d", "w", "left shift"),
            2: PlayerBindings("left", "right", "up", "right shift"),
        }
    )

    # Presentation
    background: tuple[int, int, int] = (0, 0, 0)
    ship_colors: tuple[tuple[int, int, int], tuple[int, int, int]] = (
        (90, 200, 255),
        (255, 150, 90),
    )
    missile_colors: tuple[tuple[int, int, int], tuple[int, int, int]] = (
        (90, 200, 255),
        (255, 150, 90),
    )
