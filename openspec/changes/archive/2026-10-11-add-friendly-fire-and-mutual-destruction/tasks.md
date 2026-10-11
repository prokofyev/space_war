## 1. Configuration

- [x] 1.1 Change `destruction_pause` default from `1.0` to `2.0` and add `fire_cooldown` (default `0.2`) in `space_war/config.py`; verify `tests/test_config.py` passes with the new values
- [x] 1.2 Update `tests/conftest.py` small config to pin `fire_cooldown` and a test-friendly `destruction_pause`; verify the fixture builds a `World` without error

## 2. Missile arming and friendly fire

- [x] 2.1 Add arming state to `Missile` in `space_war/entities.py` (armed once it first leaves its owner's collision radius); verify a new unit test constructs and defaults it correctly
- [x] 2.2 Update `_resolve_missile_ship_hits` in `space_war/world.py` to consider the owner ship, skipping destruction only while the missile has not yet armed; verify a test shows a fresh missile spares its ship and a returned armed missile destroys it
- [x] 2.3 Update `_resolve_missile_interceptions` to allow same-owner pairs; verify a test fires two same-owner missiles into overlap and asserts both are removed with no ship damage

## 3. Fire cooldown

- [x] 3.1 Add per-player cooldown state to `World`, decrement it in `_apply_controls`, and gate `_fire` on it; verify a test shows a second press inside the cooldown creates no missile and a press after the cooldown does
- [x] 3.2 Reset cooldown state in `reset_round`; verify a test checks cooldown is cleared at round start

## 4. Round-end window and scoring

- [x] 4.1 Rework `World.step` so the round-end window keeps applying controls, firing, movement, wrapping, expiry, and missile damage instead of short-circuiting; verify a test shows a missile fired or already in flight during the window still destroys the other ship
- [x] 4.2 Change `_resolve_round` to score the opponent of every newly dead ship once per round and start a single non-restarting countdown at the first death; verify a mutual-destruction test asserts `scores == [1, 1]` and the round closes after exactly one window
- [x] 4.3 Ensure the window timer does not restart when the second ship dies and that no further scoring happens after it elapses; verify a timing test advances in sub-steps and asserts the respawn point

## 5. Verification

- [x] 5.1 Update and run `tests/test_missiles.py`, `tests/test_match_flow.py`, `tests/test_gravity.py`, and `tests/test_effects.py`; verify the full suite passes with `uv run pytest -q`
- [x] 5.2 Run `openspec validate add-friendly-fire-and-mutual-destruction --strict` and verify the change is valid
