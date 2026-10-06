"""Minimal 2D vector helpers operating on plain ``(x, y)`` tuples."""
from __future__ import annotations

import math

Vec = tuple[float, float]


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1])


def scale(a: Vec, s: float) -> Vec:
    return (a[0] * s, a[1] * s)


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1]


def length(a: Vec) -> float:
    return math.hypot(a[0], a[1])


def normalize(a: Vec) -> Vec:
    n = length(a)
    if n == 0.0:
        return (0.0, 0.0)
    return (a[0] / n, a[1] / n)


def from_angle(angle: float) -> Vec:
    return (math.cos(angle), math.sin(angle))
