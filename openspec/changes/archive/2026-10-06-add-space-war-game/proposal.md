## Why

The project is an empty Python scaffold (`main.py` prints a greeting). There is
no game yet. We want a local, dependency-light two-player arcade in which two
people share one keyboard and pilot inertia-driven ships against each other.
Bulding an explicit spec of the physics, controls, and round rules first keeps
the Newtonian movement and collision behavior unambiguous before any code is
written.

## What Changes

- Add a runnable Pygame application (new `space_war` package, launched from
  `main.py`) that opens a fullscreen display hosting a two-player match, with
  the playfield sized to the screen resolution and Escape to quit.
- Add two player-controlled ships with Newtonian inertia: rotate
  clockwise/counter-clockwise, thrust forward while the key is held, drift when
  coasting. Thrust accelerates or brakes the ship depending on the angle between
  its velocity vector and its thrust direction.
- Add a borderless toroidal playfield: leaving one edge re-enters at the
  opposite edge, for ships and missiles alike.
- Add elastic ship-vs-ship collisions modeled as billiard balls of equal mass
  (momentum and kinetic energy conserved, no damage dealt).
- Add missiles fired with player-specific Shift keys: limited magazine (starts
  at 3), slow automatic replenishment, lifetime-limited flight that self-destructs
  when it expires, and a hit on the enemy ship that ends the round.
- Add missile-vs-missile interception so one missile can destroy another.
- Add per-round scoring and automatic round restart: when a ship is destroyed,
  the opponent gains a point and both ships respawn.
- Add per-player controls documentation and a config module for tunable physics
  and combat constants.
- Add tests for the pure simulation logic (movement, wrap, collisions, missile
  lifecycle) that run without opening a window.

## Capabilities

### New Capabilities
- `space-war/ship-movement`: Newtonian ship motion, rotation, thrust/brake
  behavior, toroidal field wrapping, and ship-vs-ship elastic collisions.
- `space-war/missiles`: per-player firing controls, ammunition and
  replenishment, missile flight lifetime, and missile interactions (hit ship,
  intercept missile).
- `space-war/match-flow`: fullscreen display, round lifecycle, scoring,
  respawn/restart, and the overall game loop and render/input responsibilities.
- `space-war/configuration`: tunable gameplay constants and per-player keyboard
  control bindings exposed as documented configuration.

### Modified Capabilities
<!-- No existing capabilities; this is a greenfield project. -->

## Impact

- New `space_war` package (simulation, rendering, input, config) plus a Pygame
  application entry point.
- `main.py` changes from a greeting script to the game launcher.
- `pyproject.toml` gains a `pygame` runtime dependency.
- New tests under `tests/` covering headless simulation logic.
