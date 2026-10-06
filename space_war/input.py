"""Translate Pygame keyboard state into per-player :class:`Controls`.

This module is the only place that reads key codes. Edge-triggered firing is
derived from the previous frame so holding the fire key does not dump the whole
magazine at once.
"""
from __future__ import annotations

import pygame

from .config import GameConfig
from .world import Controls


class InputMapper:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self._codes = {
            player: {
                "rotate_ccw": pygame.key.key_code(bindings.rotate_ccw),
                "rotate_cw": pygame.key.key_code(bindings.rotate_cw),
                "thrust": pygame.key.key_code(bindings.thrust),
                "fire": pygame.key.key_code(bindings.fire),
            }
            for player, bindings in config.player_bindings.items()
        }
        self._prev_fire = [False, False]

    def poll(self) -> list[Controls]:
        pressed = pygame.key.get_pressed()
        controls: list[Controls] = []
        for player in (1, 2):
            codes = self._codes[player]
            rotate = 0
            if pressed[codes["rotate_ccw"]]:
                rotate -= 1
            if pressed[codes["rotate_cw"]]:
                rotate += 1
            fire_now = bool(pressed[codes["fire"]])
            index = player - 1
            fire = fire_now and not self._prev_fire[index]
            self._prev_fire[index] = fire_now
            controls.append(
                Controls(
                    thrust=bool(pressed[codes["thrust"]]),
                    rotate=rotate,
                    fire=fire,
                )
            )
        return controls
