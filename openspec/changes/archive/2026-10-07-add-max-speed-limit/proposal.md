## Why

Ships currently have no speed ceiling: `world._apply_controls` keeps adding
thrust straight to velocity forever, so holding the thrust key accelerates
without bound and a ship eventually crosses the whole screen in a few frames as
an unplayable blur. We want a principled ceiling, not an arbitrary wall: a
special-relativity model in which a body's relativistic mass grows with speed
(`m = gamma * m0`), so a finite force produces ever-less acceleration and no
object can ever reach the speed of light.

## What Changes

- Model motion with special relativity: each object has a rest mass, and
  relativistic momentum `p = gamma * m0 * v`. Force/thrust changes momentum
  (`dp = F * dt`), and velocity is derived from momentum, so speed approaches
  the speed of light `c` asymptotically and can never reach or exceed it.
- Apply this to ships: thrust adds momentum along the facing direction, so
  acceleration diminishes near `c` (relativistic mass growth) while braking and
  steering still work.
- Apply it to ship-ship collisions: resolve them as relativistic elastic
  collisions of equal rest mass in the center-of-momentum frame, conserving
  relativistic momentum and energy, with no need for an arbitrary velocity cap.
- Apply it to missiles: their launch velocity is the relativistic addition of
  the ship's velocity and the muzzle velocity, so a missile never exceeds `c`
  and no longer relies on a clipped vector sum.
- Add configuration for the speed of light `c` (and reuse the existing rest
  mass). Debris, being purely visual, is exempt.

## Capabilities

### New Capabilities
<!-- None: this refines existing movement/missile behavior. -->

### Modified Capabilities
- `space-war/ship-movement`: motion follows relativistic momentum/energy; ships
  cannot reach or exceed the speed of light; ship-ship collisions are
  relativistic elastic.
- `space-war/missiles`: missile launch uses relativistic velocity addition and
  can never exceed the speed of light.
- `space-war/configuration`: a new tunable speed-of-light constant.

## Impact

- `space_war/config.py` gains `speed_of_light` (`c`); rest mass already exists.
- `space_war/world.py` gains relativistic helpers (gamma, momentum<->velocity,
  velocity addition) used by thrust, collisions, and missile launch.
- Tests: new relativistic-dynamics and collision tests; the earlier
  "asymptotic blend / collision cap" approach is replaced by exact SR.
