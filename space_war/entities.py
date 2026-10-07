"""Mutable simulation state for ships and missiles."""
from __future__ import annotations

from dataclasses import dataclass

from .vector import Vec


@dataclass
class Ship:
    position: Vec
    velocity: Vec = (0.0, 0.0)
    angle: float = 0.0
    alive: bool = True


@dataclass
class Missile:
    position: Vec
    velocity: Vec
    owner: int            # index of the player who fired it (0 or 1)
    age: float = 0.0      # seconds in flight
