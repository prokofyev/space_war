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

    Field dimensions are intentionally absent: the world is infinite, so the
    simulation has no bounds and the display size only affects the camera.
    """

    # Ship physics
    ship_radius: float = 32.0
    ship_mass: float = 1.0              # rest mass of a ship
    rotation_speed: float = 3.4          # radians / second
    thrust_accel: float = 320.0          # low-speed acceleration; force = accel * mass

    # Relativity
    speed_of_light: float = 1000.0       # pixels / second; no object may reach it

    # Missiles
    missile_speed: float = 620.0         # pixels / second added along facing
    missile_radius: float = 4.0
    missile_lifetime: float = 13.5        # seconds in flight before self-destruct
    missile_mass: float = 0.02           # gravitational mass of a missile

    # Gravity
    gravitational_constant: float = 1.0e6  # G; scales all mutual attraction
    gravity_min_distance: float = 32.0       # soft floor for r to avoid singularities

    # Ammunition
    ammo_start: int = 3
    ammo_max: int = 3
    ammo_replenish_interval: float = 3.0  # seconds per replenished missile

    # Round timing
    destruction_pause: float = 2.0       # seconds of round-end window before respawn

    # Firing
    fire_cooldown: float = 0.2           # seconds between two shots from one player

    # Presentation: explosion and effects
    debris_count: int = 14
    debris_speed: float = 170.0          # pixels / second, initial outward speed
    debris_min_speed: float = 60.0
    debris_lifetime: float = 0.9         # seconds before a piece disappears
    debris_size: float = 3.5             # pixels
    debris_damping: float = 2.0          # velocity decay per second
    trail_length: float = 26.0           # pixels of missile trail
    trail_points: int = 6
    glow_radius: float = 22.0            # pixels of halo around a ship
    glow_steps: int = 18
    ship_sprite_scale: float = 2.6      # ship image length as a multiple of ship_radius

    # Spawn: the two ships start centered on the origin, separated along the
    # horizontal axis by this many world units, facing each other.
    initial_ship_distance: float = 960.0
    start_facings: tuple[float, float] = (0.0, math.pi)

    # Camera: fraction of the viewport kept as border around the framed ships,
    # and the exponential smoothing rate (per second) for zoom/pan changes.
    camera_margin: float = 0.15
    camera_smoothing: float = 6.0

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
