## 1. Configuration

- [x] 1.1 Add `speed_of_light` (`c`) to `space_war/config.py` and document
  `ship_mass` as rest mass; choose a default `c` high enough that typical play
  stays Newtonian. Verify with a test that `c > 0`.
- [x] 1.2 Add a test that low-speed behavior is preserved: with `|v| << c`, a
  thrust step still produces approximately the Newtonian acceleration.
- [x] 1.3 Decide and document how thrust force relates to the old
  `thrust_accel` (e.g. `F = thrust_accel * ship_mass`) and add a test asserting
  the low-speed equivalence.

## 2. Relativistic helpers

- [x] 2.1 Implement `gamma(v)`, `momentum(v)`, and
  `velocity_from_momentum(p)` in a small module (or `world.py`); verify
  `|velocity_from_momentum(momentum(v)) - v|` is tiny for many speeds and that
  `|velocity_from_momentum(p)| < c` for large `p`.
- [x] 2.2 Guard against `v -> c` numerically (epsilon clamp) and verify no NaN /
  infinity is produced for extreme inputs.

## 3. Thrust as force

- [x] 3.1 Change `_apply_controls` to add momentum `F * dt` along the facing
  direction and derive velocity from momentum; verify sustained thrust approaches
  `c` asymptotically and stays strictly below it.
- [x] 3.2 Verify diminishing acceleration near `c`: the same thrust at high speed
  adds less speed than at low speed.
- [x] 3.3 Verify braking still works near `c`: thrust opposite velocity reduces
  speed.
- [x] 3.4 Verify perpendicular thrust still deflects near `c`.
- [x] 3.5 Verify frame-rate independence: the same total thrust time at different
  `dt` yields the same speed within tolerance (sub-step if needed).

## 4. Relativistic collisions

- [x] 4.1 Resolve ship-ship collisions in the center-of-momentum frame by
  reversing each body's momentum, then transform back; verify total relativistic
  momentum and energy are conserved and both speeds stay below `c`.
- [x] 4.2 Verify the low-speed limit matches the Newtonian equal-mass result
  (velocity exchange) within tolerance, and that no ship is destroyed and no
  score changes.

## 5. Missiles

- [x] 5.1 Compute missile launch velocity with relativistic velocity addition of
  the ship velocity and the muzzle velocity along facing; verify a missile fired
  from a near-`c` ship stays strictly below `c`.
- [x] 5.2 Verify the low-speed launch velocity approximately equals the naive sum
  (ship velocity plus muzzle velocity).
- [x] 5.3 Verify in-flight missiles never exceed `c`.

## 6. Verification and docs

- [x] 6.1 Run `uv run pytest -q` and confirm all movement, collision, missile,
  and match tests pass with the relativistic model.
- [x] 6.2 Add/extend tests covering: gamma/mass growth, unreachable `c`,
  diminishing acceleration, braking and steering near `c`, SR collision
  conservation, low-speed Newtonian equivalence, and missile capping.
- [x] 6.3 Update `README.md` and config docs to describe the relativistic model
  and the new `speed_of_light` tunable.
