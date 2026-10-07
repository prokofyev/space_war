import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

pygame.init()


class _FakePressed:
    """Stand-in for pygame.key.get_pressed() indexed by key code."""

    def __init__(self, pressed_codes):
        self._pressed = set(pressed_codes)

    def __getitem__(self, code):
        return code in self._pressed


import pytest  # noqa: E402

from dataclasses import replace  # noqa: E402

from space_war.config import GameConfig  # noqa: E402
from space_war.world import World  # noqa: E402


@pytest.fixture
def fake_key(monkeypatch):
    def install(codes):
        fake = _FakePressed(codes)
        monkeypatch.setattr("pygame.key.get_pressed", lambda: fake)
        return fake

    return install


@pytest.fixture
def small_config():
    return replace(
        GameConfig(),
        ship_radius=5.0,
        ship_mass=1.0,
        rotation_speed=2.0,
        thrust_accel=10.0,
        missile_speed=50.0,
        missile_radius=2.0,
        missile_lifetime=1.0,
        ammo_start=3,
        ammo_max=3,
        ammo_replenish_interval=1.0,
        start_positions=((0.1, 0.1), (0.9, 0.9)),
        start_facings=(0.0, 0.0),
        # Gravity is exercised by dedicated tests; mechanic tests isolate
        # bodies so coasting stays a straight line.
        gravitational_constant=0.0,
    )


@pytest.fixture
def world(small_config):
    return World(config=small_config, width=100.0, height=100.0)
