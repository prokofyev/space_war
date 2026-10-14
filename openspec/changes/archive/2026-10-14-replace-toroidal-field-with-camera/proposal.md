## Why

The playfield is currently a torus the size of the display: any ship that
crosses an edge reappears on the opposite side, and gravity, collisions, and
missile flight all measure distances through that wrap. This makes the world
finite and the seam silently teleports ships, so it is impossible to keep the
two ships framed together. Replacing the torus with an infinite world viewed
through a smoothly zooming camera keeps both ships on screen at all times.

## What Changes

- **BREAKING** Remove the borderless toroidal field and its edge wrapping: the
  world becomes an ordinary infinite plane. Ships and missiles no longer wrap.
- **BREAKING** Remove `start_positions` in display fractions; add a configurable
  `initial_ship_distance` (world units) and derive both start positions from it,
  centered on the origin and mirrored so the ships face each other.
- **BREAKING** `World` no longer derives its dimensions from the display
  resolution; the world is unbounded and gravity, collisions, and missile
  distances become plain Euclidean distances.
- Add a camera to the render layer that centers on the midpoint between the two
  ships and scales the view so both ships always fit on screen with a margin,
  adjusting smoothly.
- The zoom has no upper cap: the camera keeps fitting both ships, so when the
  ships are far apart it zooms out, and when they are close it zooms in and
  magnifies them. The initial zoom is derived from `initial_ship_distance`.
- Missiles are not required to stay on screen; the camera framing requirement
  covers the two ships only.

## Capabilities

### New Capabilities
<!-- None. -->

### Modified Capabilities
- `space-war/ship-movement`: the borderless toroidal playfield requirement is
  replaced by an infinite plane with no wrapping.
- `space-war/gravity`: gravitational distances are Euclidean rather than
  toroidal, and the purpose no longer references the borderless field.
- `space-war/match-flow`: the fullscreen requirement no longer ties playfield
  dimensions to the display resolution, and the round-lifecycle scenarios that
  mention edge wrapping must drop it.
- `space-war/configuration`: `start_positions` is replaced by
  `initial_ship_distance`, and field dimensions are no longer derived from the
  display.
- `space-war/visuals`: adds the smoothly zooming camera that keeps both ships
  framed.
- `space-war/missiles`: the missile-flight requirement drops the "missile
  crosses the borderless field" scenario, since the field is now infinite.

## Impact

- `space_war/world.py`: drop `wrap_scalar`, `toroidal_delta`, `_wrap_ships`,
  `_wrap_missiles`, `_size`, and display-derived `width`/`height`; use Euclidean
  distances for gravity, collisions, and hit tests; respawn positions come from
  `initial_ship_distance`.
- `space_war/game.py`: `world_from_display` no longer sizes the world from the
  surface; construct an unbounded world instead.
- `space_war/render.py`: new camera (pan to midpoint, smooth zoom-to-fit both
  ships, one shared scale for both axes) applied to drawing; scores stay on the
  HUD.
- `space_war/config.py`: remove `start_positions`, add `initial_ship_distance`
  plus camera framing constants (margin and smoothing rate).
- Tests: `tests/test_field_dimensions.py`, `tests/test_collisions.py`,
  `tests/test_gravity.py`, `tests/test_missiles.py`, `tests/test_movement.py`,
  `tests/test_render_smoke.py`, and any test relying on wrapping or a
  display-sized world.
- No new dependencies; the simulation stays headless and deterministic.
