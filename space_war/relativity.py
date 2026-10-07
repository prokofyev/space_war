"""Special-relativity helpers for the simulation.

Velocities are stored as plain 2D vectors, but the physics works through
momentum: with rest mass ``m0`` and speed of light ``c``,

    gamma(v) = 1 / sqrt(1 - (|v| / c)^2)
    p(v)     = gamma(v) * m0 * v
    v(p)     = p / sqrt(m0^2 + |p|^2 / c^2)

The inverse ``velocity_from_momentum`` is closed-form and guarantees ``|v| < c``
for any finite momentum, so no object can ever reach the speed of light.
"""
from __future__ import annotations

import math

from .vector import Vec, add, dot, length, scale, sub

_EPS = 1e-9


def gamma(speed: float, c: float) -> float:
    """Lorentz factor for a scalar speed, guarded against reaching ``c``."""
    ratio = min(abs(speed) / c, 1.0 - _EPS)
    return 1.0 / math.sqrt(max(1e-18, 1.0 - ratio * ratio))


def momentum(velocity: Vec, rest_mass: float, c: float) -> Vec:
    """Relativistic momentum ``p = gamma * m0 * v``."""
    g = gamma(length(velocity), c)
    return scale(velocity, g * rest_mass)


def velocity_from_momentum(p: Vec, rest_mass: float, c: float) -> Vec:
    """Velocity from momentum; always returns a speed strictly below ``c``."""
    denom = math.sqrt(rest_mass * rest_mass + dot(p, p) / (c * c))
    if denom == 0.0:
        return (0.0, 0.0)
    v = scale(p, 1.0 / denom)
    speed = length(v)
    limit = c * (1.0 - _EPS)
    if speed >= limit:
        v = scale(v, limit / speed)
    return v


def energy(p: Vec, rest_mass: float, c: float) -> float:
    """Total relativistic energy ``E = sqrt((|p| c)^2 + (m0 c^2)^2)``."""
    pc = length(p) * c
    m0c2 = rest_mass * c * c
    return math.sqrt(pc * pc + m0c2 * m0c2)


def boost(p: Vec, e: float, frame_velocity: Vec, c: float) -> tuple[Vec, float]:
    """Lorentz-boost momentum/energy into a frame moving at ``frame_velocity``.

    Standard transform (``v = frame_velocity``, ``v_hat`` its direction)::

        E' = gamma (E - v . p)
        p'_parallel = gamma (p_parallel - (v/c^2) E)
        p'_perp = p_perp
    """
    speed = length(frame_velocity)
    if speed == 0.0:
        return p, e
    v_hat = scale(frame_velocity, 1.0 / speed)
    g = gamma(speed, c)
    p_par_scalar = dot(p, v_hat)
    p_par = scale(v_hat, p_par_scalar)
    p_perp = sub(p, p_par)
    e_new = g * (e - speed * p_par_scalar)
    p_par_new = scale(sub(p_par, scale(v_hat, speed * e / (c * c))), g)
    p_new = add(p_par_new, p_perp)
    return p_new, e_new


def add_velocities(u: Vec, v: Vec, c: float) -> Vec:
    """Relativistic velocity addition: ``u`` in a frame moving at ``v``.

    ``u`` is the velocity in the moving frame (e.g. a missile's muzzle velocity
    relative to its ship) and ``v`` is that frame's velocity in the field.
    """
    speed_v = length(v)
    if speed_v == 0.0:
        return u
    v_hat = scale(v, 1.0 / speed_v)
    u_par_scalar = dot(u, v_hat)
    u_par = scale(v_hat, u_par_scalar)
    u_perp = sub(u, u_par)
    denom = 1.0 + dot(u, v) / (c * c)
    if denom <= 0.0:
        denom = _EPS
    w_par = scale(add(u_par, v), 1.0 / denom)
    w_perp = scale(u_perp, 1.0 / (gamma(speed_v, c) * denom))
    return add(w_par, w_perp)
