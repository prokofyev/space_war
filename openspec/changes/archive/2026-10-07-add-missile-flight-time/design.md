## Context

See `proposal.md` - Why. `space_war/entities.py` `Missile` currently carries
`traveled` (pixels); `space_war/world.py` `_integrate_missiles` accumulates
`|velocity| * dt` and `_expire_missiles` drops missiles once
`traveled >= config.missile_range`. Missiles inherit the ship's velocity via
relativistic addition, so their speed varies and a distance bound gives an
inconsistent lifetime. The simulation is window-free and unit-tested.

The behavior contract is the deltas in `space-war/missiles` and
`space-war/configuration`.

## Goals / Non-Goals

**Goals:**

- Bound a missile's life by a fixed time in seconds.
- Keep the change minimal and localized to missile state, expiry, config, and
  tests/docs.

**Non-Goals:**

- Changing launch speed, relativistic addition, interception, or hit rules.
- The maximum-speed / `c` value (that is a separate, already-made change).
- Debris or explosion behavior.

## Decisions

**Track age in seconds, not distance.** Replace `Missile.traveled` (pixels) with
`Missile.age` (seconds). `_integrate_missiles` adds `dt` to `age`;
`_expire_missiles` drops missiles whose `age >= missile_lifetime`. This makes
lifetime independent of a missile's speed, which is the requested behavior.
Alternative: keep `traveled` and derive time from it - rejected because it is
exactly the speed-dependent behavior we are removing.

**Config rename `missile_range` (px) -> `missile_lifetime` (s), default 1.5.**
1.5 s at the base launch speed (~620 px/s) is ~930 px, matching the previous
~900 px feel. Alternative: keep the old name and change units - rejected as a
silent unit change is a footgun; an explicit rename is clearer.

**No cap interaction.** Missile speed is already bounded by `c` at launch, so a
time bound stays well-defined. No change to `_fire`.

## Risks / Trade-offs

- [Behavioral change for fast ships] A missile fired from a fast ship now lives
  the same time but travels farther -> intended; a scenario asserts this.
- [Silent unit confusion] Pixels vs seconds on the same field name -> mitigated
  by renaming the field and constant.
- [Test fixtures] Several tests construct `Missile(traveled=...)` -> must be
  updated to `age=`; forgetting one yields a confusing failure -> covered by the
  test-update task.

## Migration Plan

Small in-place refactor: rename the missile field and the config constant, change
integration/expiry to time, update tests and docs. No data migration; old configs
using `missile_range` would need the rename (documented).

## Open Questions

- None blocking. The default 1.5 s is a tuning choice adjustable in config.
