## 1. Configuration

- [x] 1.1 Add visual and timing fields to `space_war/config.py`
  (`destruction_pause` default 1.0, `debris_count`, `debris_speed`,
  `debris_lifetime`, `flame_length`, `flame_animation_speed`, `trail_length`,
  `glow_radius`, plus any radii) with defaults so existing configs keep working;
  verify a default `GameConfig()` still constructs and `tests/test_config.py`
  passes.
- [x] 1.2 Add a unit test asserting `destruction_pause > 0` and that visual
  fields have sane positive defaults.

## 2. Ship sprite generation

- [x] 2.1 Create `space_war/sprites.py` with `build_ship_surface(config, player)`
  that procedurally draws an anti-aliased ship with a distinct nose, fins, and
  exhaust nozzle, depth shading (lighter top, darker bottom), and a cockpit
  accent, pre-rendered at 4x and downscaled; verify the returned surface is
  non-empty and larger than the ship radius in both dimensions.
- [x] 2.2 Add `build_glow_surface(config, player)` producing a soft radial halo;
  verify it is a surface with per-pixel alpha.
- [x] 2.3 Add tests that sprites are generated for both player colours and that
  the two sprites differ (players stay distinguishable).

## 3. Sprite-based rendering

- [x] 3.1 Update `space_war/render.py` to draw each ship by rotating its
  pre-rendered sprite with `pygame.transform.rotozoom` to match the ship angle
  (including correct handedness) instead of the flat ring + facing line; verify
  orientation reads correctly with a headless test that the rotated sprite
  differs across two angles.
- [x] 3.2 Draw the glow halo behind each ship using its player colour; verify
  the ship draw path still runs headlessly for both players.
- [x] 3.3 Keep the existing score/ammo HUD working and verify
  `tests/test_render_smoke.py` still passes.

## 4. Thrust flame and missile trail

- [x] 4.1 Draw an animated flame from the ship nozzle opposite the facing
  direction only while thrust is held, with animation driven by elapsed time;
  verify no flame is drawn when thrust is not held (headless test on the render
  helper).
- [x] 4.2 Draw a fading trail behind each missile along the reverse of its
  velocity; verify the render path accepts a world with an in-flight missile.
- [x] 4.3 Verify the flame/trail additions do not change simulation results:
  `uv run pytest -q` still green, especially collision/missile/score tests.

## 5. Explosion and round-end pause

- [x] 5.1 Add the destruction pause to `World`: on ship destruction stop
  scoring, hold a configurable `destruction_pause`, and only then `reset_round()`;
  expose the destroyed ship (index, position, angle) to the render layer for the
  frame. Verify with a test that no respawn happens before the pause elapses and
  respawn happens after it.
- [x] 5.2 Verify scoring is unchanged by the pause: the winner gains exactly one
  point and the score from the delayed round matches the non-delayed case.
- [x] 5.3 Implement debris in the render layer: spawn pieces on a destruction
  event with differing outward directions and speeds, update them with `dt`
  (decelerate and fade), and drop them after `debris_lifetime`; verify debris
  spawns on destruction and is gone after its lifetime.
- [x] 5.4 Clear debris and explosion state on any round reset; verify no debris
  from a previous round remains after respawn.
- [x] 5.5 Verify debris is purely visual: ships/missiles/scoring are unaffected
  while debris is active.

- [x] 5.6 Keep the world advancing during the destruction pause: surviving ships
  keep their momentum and in-flight missiles keep flying, wrapping, and expiring
  while only the respawn is delayed; verify with a test that a missile moves
  during the pause and a coasting survivor keeps its velocity.
- [x] 5.7 Give the destruction event the ship's velocity and add it to each
  debris piece so the cloud drifts with the ship's momentum; verify with a test
  that debris from a moving ship carries that velocity.

## 6. Integration and docs

- [x] 6.1 Wire the destruction event from `World` through `game.py` into the
  render layer and verify a full run works headlessly under the dummy SDL driver
  (spawn, destroy, debris, respawn) without errors.
- [x] 6.2 Manually run `uv run python main.py`: confirm readable ship
  orientation, glow, thrust flame, missile trails, and a visible explosion with
  debris before the new round starts.
- [x] 6.3 Update `README.md` to mention the new visuals and the
  destruction-pause behavior, and document any new tunable config values.
