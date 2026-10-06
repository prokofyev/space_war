## 1. Project setup

- [x] 1.1 Add `pygame` to runtime dependencies and `pytest` to dev
  dependencies in `pyproject.toml`, then run `uv sync` and verify it succeeds.
- [x] 1.2 Create the `space_war` package (`__init__.py`) and the `tests/`
  directory, and verify `uv run python -c "import space_war"` succeeds.

## 2. Configuration

- [x] 2.1 Implement `space_war/config.py` with a `GameConfig` dataclass covering
  field size, ship radius/mass/rotation rate/thrust acceleration, missile launch
  speed/radius/range, ammo start/max/replenish interval, start positions/facings,
  and per-player key bindings; verify a default config and a tiny test config can
  both be constructed (spec: `space-war/configuration`).
- [x] 2.2 Verify the two ships share equal mass and the two players' bindings are
  disjoint with a unit test (spec: equal mass, distinct bindings).

## 3. Simulation core

- [x] 3.1 Implement `space_war/entities.py` `Ship` and `Missile` state and
  `space_war/world.py` with `World.step(dt, controls)` integrating rotation,
  thrust-along-facing, and `position += velocity * dt`; verify coasting keeps
  velocity and thrust along facing increases speed (spec: `space-war/ship-movement`).
- [x] 3.2 Add the toroidal wrap for ships and verify exiting each edge re-enters
  at the opposite edge with unchanged velocity/facing, including a diagonal
  corner case (spec: toroidal playfield).
- [x] 3.3 Verify thrust brakes when facing opposite velocity, accelerates when
  facing along it, and deflects the course when perpendicular, with unit tests
  (spec: thrust relative to velocity).
- [x] 3.4 Implement the ship-vs-ship equal-mass elastic collision with
  post-collision separation, and verify head-on velocity exchange plus total
  momentum and kinetic energy conservation in glancing collisions with no score
  change (spec: damage-free elastic ship collision).
- [x] 3.5 Add the toroidal distance helper and use it for all collision
  proximity checks, and verify a collision across the seam is detected with a
  unit test.

## 4. Missiles

- [x] 4.1 Implement firing in `World.step`: spawn a missile at the ship position
  along facing with launch speed combined with ship velocity, consume one round
  from the magazine, and verify an empty magazine fires nothing (spec:
  `space-war/missiles`).
- [x] 4.2 Implement ammunition replenishment with a float accumulator, verify it
  adds one missile per interval, never exceeds the max of three, and resets on
  round start (spec: ammunition and replenishment).
- [x] 4.3 Implement missile straight-line flight, `dt`-driven wrap, and
  lifetime/range expiry removal with no score change; verify with unit tests
  (spec: flight lifetime and self-destruct).
- [x] 4.4 Implement missile-vs-enemy-ship hits: consume the missile, destroy the
  enemy ship, award one point, and reset the round; verify the firing player's
  own ship is never hit by their missile (spec: missile destroys an enemy ship).
- [x] 4.5 Implement missile-vs-missile interception: remove both missiles with
  no score change; verify with a unit test (spec: missile intercepts another
  missile).
- [x] 4.6 Enforce the deterministic per-step update ordering from design.md and
  verify no double-scoring or expiry-then-hit happens in a single step with a
  unit test.

## 5. Match flow

- [x] 5.1 Implement score persistence, round end on a single ship's
  destruction, and automatic respawn of both ships with zero velocity, defined
  facing, cleared missiles, and reset magazines (spec: `space-war/match-flow`).
- [x] 5.2 Verify scores accumulate across rounds and the surviving player gets
  exactly one point with a multi-round unit test.

## 6. Input, rendering, and application

- [x] 6.1 Implement `space_war/input.py` producing per-player `Controls` with
  level-triggered thrust/rotate and edge-triggered fire; verify with a unit test
  that a held key yields fire once and that bindings map to the correct player.
- [x] 6.2 Implement `space_war/render.py` drawing both ships, all missiles, and
  both scores, and verify the game renders in a manual run.
- [x] 6.3 Implement `space_war/game.py` to open the display in fullscreen mode,
  derive the `World` field size from the display resolution, and run a `dt`-driven
  event loop that exits cleanly on the Escape key or quit event while clamping
  large `dt` after stalls; verify with a unit test that the field dimensions are
  taken from a supplied display size.
- [x] 6.4 Repoint `main.py` at the game launcher and verify by running
  `uv run python main.py`: the game fills the screen with no window borders,
  runs a round, and Escape exits cleanly.

## 7. Verification

- [x] 7.1 Run the full headless test suite with `uv run pytest -q` and verify all
  simulation tests pass without opening a window.
- [x] 7.2 Manually play a two-player match and confirm the game fills the screen
  in fullscreen, controls respond, both players wrap through all edges, missiles
  self-destruct, ship hits score and restart, missiles can intercept each other,
  ship collisions bounce without damage, and Escape quits cleanly.
- [x] 7.3 Update `README.md` to document the controls (including Escape to
  quit), the fullscreen behavior, how to run the game, and the tunable
  `GameConfig` values.
