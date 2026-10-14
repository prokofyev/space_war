## 1. Configuration

- [x] 1.1 In `space_war/config.py`, replace `start_positions` with `initial_ship_distance` (default equal to the current 0.5-screen separation expressed in world units) and add `camera_margin` and `camera_smoothing`; verify `tests/test_config.py` passes
- [x] 1.2 Update `tests/conftest.py` to set `initial_ship_distance` and camera values for the small config; verify the `world` fixture still builds

## 2. Unbounded world

- [x] 2.1 In `space_war/world.py`, remove `width`/`height`, `wrap_scalar`, `toroidal_delta`, `_size`, `_wrap_ships`, and `_wrap_missiles`; make `distance` the Euclidean norm; verify `tests/test_collisions.py` passes with Euclidean expectations
- [x] 2.2 Update `reset_round` to spawn ships from `initial_ship_distance` symmetrically about the origin; verify a test asserts the separation equals the configured distance and the facings point at each other
- [x] 2.3 Switch gravity and all collision/hit tests to Euclidean deltas; verify `tests/test_gravity.py` passes with the straight-line distance and no wrapping scenarios
- [x] 2.4 Update `space_war/game.py` so `world_from_display` no longer sizes the world from the surface but returns an unbounded world; verify `tests/test_field_dimensions.py` is updated accordingly
- [x] 2.5 Remove or rewrite now-invalid wrapping tests in `tests/test_movement.py` and `tests/test_missiles.py`; verify the full suite passes with `uv run pytest -q`

## 3. Camera

- [x] 3.1 Add a camera to `space_war/render.py` that tracks the midpoint of the two ships, computes a target uniform scale that fits both ships with `camera_margin`, initializes the scale from `initial_ship_distance`, and smooths toward the target using `camera_smoothing`; verify a unit test shows the ships' projections stay inside the viewport
- [x] 3.2 Route all world drawing (ships, missiles, trails, debris) through the camera transform, and keep the scores HUD in screen space; verify `tests/test_render_smoke.py` passes and a test asserts both ships are on screen after they separate
- [x] 3.3 Verify zoom is uncapped and uniform: a test asserts the scale grows when the ships are close and that the X and Y scales are equal

## 4. Verification

- [x] 4.1 Run the full suite with `uv run pytest -q` and fix any remaining wrapping or dimension assumptions
- [x] 4.2 Run `openspec validate replace-toroidal-field-with-camera --strict` and verify the change is valid
