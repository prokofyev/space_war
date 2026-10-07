## 1. Configuration and entity state

- [x] 1.1 In `space_war/config.py`, rename `missile_range` to
  `missile_lifetime` with a default of 1.5 (seconds) and update the comment;
  verify the module imports and `GameConfig()` constructs.
- [x] 1.2 In `space_war/entities.py`, replace `Missile.traveled` (pixels) with
  `age` (seconds); verify the module imports.

## 2. Simulation

- [x] 2.1 In `space_war/world.py`, update `_fire` to construct missiles with
  `age=0.0`, update `_integrate_missiles` to add `dt` to `age`, and update
  `_expire_missiles` to drop missiles whose `age >= missile_lifetime`.
- [x] 2.2 Verify with a unit test that a missile is removed after exactly the
  configured lifetime of flight time, and not before.
- [x] 2.3 Verify that two missiles with different speeds are both removed after
  the same elapsed flight time (faster one travels farther), proving the bound
  is time-based.

## 3. Update tests

- [x] 3.1 Update `tests/conftest.py` and any tests that reference
  `missile_range` or `Missile(traveled=...)` (`tests/test_missiles.py`,
  `tests/test_step_ordering.py`, `tests/test_match_flow.py`,
  `tests/test_relativity.py`) to the new `missile_lifetime` / `age` fields.
- [x] 3.2 Run `uv run pytest -q` and confirm the whole suite passes.

## 4. Docs

- [x] 4.1 Update `README.md` to state that missiles explode after a fixed flight
  time and note the `missile_lifetime` config value in seconds.
