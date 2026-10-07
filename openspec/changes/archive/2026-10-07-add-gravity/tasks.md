## 1. Configuration and entity mass

- [x] 1.1 Add a `gravitational_constant` (`G`) and a missile gravitational mass
  to `space_war/config.py` with sensible defaults; verify `GameConfig()`
  constructs and `tests/test_config.py` passes.
- [x] 1.2 Decide how each body exposes its gravitational mass (reuse
  `ship_mass`; add a missile mass) and verify both ship and missile masses are
  available from the world for the gravity step.

## 2. Gravity force

- [x] 2.1 Implement a pairwise gravitational force in `space_war/world.py` using
  the shortest toroidal distance and `F = G * m_i * m_j / r^2`, clamped by a
  small minimum distance to avoid singularities; verify two bodies accelerate
  toward each other.
- [x] 2.2 Verify the inverse-square law with unit tests: doubling distance drops
  the force to ~1/4 and scaling a mass scales the force.
- [x] 2.3 Verify attraction works across the field edge: two bodies near
  opposite edges attract each other across the shortest wrapped path.
- [x] 2.4 Verify coincident/near-coincident bodies produce finite acceleration
  (no NaN or infinity).

## 3. Apply gravity relativistically

- [x] 3.1 Apply the net gravitational force as a momentum change
  (`p += F * dt`) for ships and missiles, deriving velocity via
  `velocity_from_momentum`; verify a body's speed stays strictly below `c` under
  strong gravity.
- [x] 3.2 Wire the gravity step into `World.step` at a deterministic point
  (before integration) for both the active round and the destruction pause, and
  verify movement/missile tests still pass.
- [x] 3.3 Verify frame-rate independence of the gravity update (same total time
  at different `dt` yields the same result within tolerance); sub-step if
  needed.

## 4. Update affected tests and docs

- [x] 4.1 Update movement/missile tests that assume a strictly straight
  coasting path or straight missile flight to account for gravity (or isolate
  them from other bodies), and run `uv run pytest -q` until green.
- [x] 4.2 Add gravity tests: all bodies attract all, missiles attract and are
  attracted, net force is the sum of pairwise forces.
- [x] 4.3 Update `README.md` to describe gravity and the new tunable constant.
