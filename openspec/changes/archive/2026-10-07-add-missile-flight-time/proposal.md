## Why

Missiles currently live for a fixed *distance* (`missile_range`, in pixels)
rather than a fixed *time*. Because a missile inherits the firing ship's
velocity through relativistic addition, its flight time varies with how fast
the ship was moving. A missile fired from a fast ship covers the same distance
in less time and feels shorter-lived, which is surprising and makes range
inconsistent round to round. Bounding a missile by a fixed lifetime in seconds
is simpler to reason about and matches the intent "the missile flies for some
time, then explodes".

## What Changes

- Bound a missile's life by a configured **time** (seconds) instead of a
  distance: a missile self-destructs when its flight time expires, regardless of
  how far it travelled.
- Track a missile's age in seconds instead of accumulated distance.
- Rename the configuration value `missile_range` (pixels) to
  `missile_lifetime` (seconds), with a default of 1.5 s (~equivalent to the old
  ~900 px at the base launch speed).
- Update documentation and tests to reflect time-based expiry.

## Capabilities

### New Capabilities
<!-- None: this refines existing missile behavior. -->

### Modified Capabilities
- `space-war/missiles`: missile lifetime is bounded by time, not distance.
- `space-war/configuration`: the missile lifetime constant is expressed in
  seconds.

## Impact

- `space_war/entities.py`: `Missile.traveled` (pixels) becomes `age` (seconds).
- `space_war/world.py`: `_integrate_missiles` advances age; `_expire_missiles`
  uses the lifetime.
- `space_war/config.py`: `missile_range` -> `missile_lifetime` (default 1.5).
- Tests and `README.md` updated.
