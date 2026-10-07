## Context

See `proposal.md` - Why. Movement lives in `space_war/world.py`:
`_apply_controls` currently adds `thrust_accel * dt` straight to `velocity`;
`_resolve_ship_collisions` exchanges normal velocity components for a Newtonian
equal-mass elastic collision; `_fire` builds a missile velocity as
`ship.velocity + missile_speed * facing`. `space_war/config.py` holds all
tunables and already has an equal `ship_mass`. `World.step` integrates per `dt`,
is window-free, and is unit-tested. Debris lives in the render layer
(`space_war/effects.py`) and is not part of the simulation.

The behavior contract is the deltas in `space-war/ship-movement`,
`space-war/missiles`, and `space-war/configuration`, which now specify exact
special relativity rather than an ad-hoc asymptotic blend.

## Goals / Non-Goals

**Goals:**

- Model special relativity exactly: relativistic mass `m = gamma * m0`, momentum
  `p = gamma * m0 * v`, and force acting as `dp/dt`.
- Guarantee no ship or missile ever reaches or exceeds the speed of light `c`.
- Keep low-speed behavior essentially Newtonian (the intuitive current feel).
- Keep the simulation deterministic, frame-rate independent, and headless
  testable.

**Non-Goals:**

- Debris: purely visual and explicitly exempt from the model.
- Gravitational effects, general relativity, or time-dilation visuals
  (no screen warp).
- Changing rotation, wrapping, ammo, scoring, or round flow.

## Decisions

**State stays in velocity; convert through momentum.** Keep the `Ship`/`Missile`
`velocity` as the source of truth (so rendering, wrapping, and tests keep
working), but perform force and collision math through momentum. Helpers:
`gamma(v) = 1 / sqrt(1 - (|v| / c)^2)`, `momentum(v) = gamma(v) * m0 * v`, and
`velocity_from_momentum(p) = p / sqrt(m0^2 + |p|^2 / c^2)`. The inverse form is
closed-form and guarantees `|v| < c` for any finite `p`. Alternative: keep
Newtonian velocity math and clamp - rejected because it is exactly the ad-hoc
wall the user does not want.

**Thrust applies force over time: `p += F * dt`.** Store thrust as a force
magnitude rather than an acceleration. Because relativistic mass grows, adding a
fixed `F * dt` of momentum yields a smaller velocity change as speed rises, so
acceleration naturally diminishes near `c`. This is the user's core requirement
("mass grows, so force cannot accelerate forever"). Frame-rate independence
falls out of integrating `dp = F * dt`; sub-step when `dt` is large for
accuracy. Alternative: `a = F / (gamma * m0)` applied to velocity - equivalent
at low order, but the momentum form is cleaner and exact.

**Braking and steering are not throttled.** Thrust opposite velocity removes
momentum along that direction and still slows the ship; perpendicular thrust
still deflects. Only growth of speed toward `c` is limited, and that limit is
automatic from `velocity_from_momentum`, not a special case.

**Relativistic elastic collision of equal rest mass.** Resolve in the
center-of-momentum frame: transform to the COM frame, where each equal-mass
body has equal-and-opposite momentum; reverse each body's momentum vector in COM,
then transform back to the field frame. This conserves relativistic momentum
and energy exactly and keeps `|v| < c`, and it reduces to the Newtonian
equal-mass result at low speed. Alternative: Newtonian normal-component swap -
rejected because at high speed it could violate `c`. Alternative: exchange
computed 4-momenta numerically - unnecessary for equal masses.

**Missiles: relativistic velocity addition.** Launch velocity is the
`tanh`/Minkowski addition of the ship's velocity and the muzzle velocity along
the facing direction (collinear-in-2D via the standard formula, applied along
the facing axis and recombined with the transverse component using the
appropriate SR transformation), which is automatically `< c`. In-flight missiles
keep constant velocity, already below `c`. Alternative: clamp the naive vector
sum - rejected as inconsistent with the SR model.

**`c` never reached, epsilon-guarded.** All conversions use `|v| < c` with a
small epsilon so floating-point arithmetic cannot land on `c`.

**Naming.** Keep `ship_mass` as the rest mass; rename its meaning in docs to rest
mass. Add `speed_of_light`. Rename `thrust_accel` semantics to a thrust force (or
document the conversion `F = thrust_accel * ship_mass` at low speed to preserve
the current feel).

## Risks / Trade-offs

- [Numerical blow-up near `c`] `gamma` diverges as `v -> c` -> use the closed-form
  momentum->velocity inverse (no division by near-zero) and clamp inputs with an
  epsilon before computing `gamma`.
- [Frame-rate sensitivity of momentum integration] Large `dt` makes `F * dt`
  inaccurate near `c` -> sub-step the momentum update when `dt` exceeds a small
  threshold; assert frame-rate independence in tests.
- [Behavior change at moderate speed] Exact SR changes handling sooner than a
  high cap would -> choose a `c` default high enough that typical play stays
  Newtonian, and cover low-speed equivalence with a test.
- [Collision complexity] SR collisions are subtler than the Newtonian swap ->
  implement COM-frame reversal and cover it with momentum/energy-conservation
  tests plus a low-speed equivalence test.
- [Feel] If `c` is too low the game feels sluggish -> make it configurable and
  document the default.

## Migration Plan

Additive behavior change replacing the Newtonian model inside the simulation.
Add `speed_of_light` to config; add SR helpers used by thrust, collisions, and
missile launch; keep `Ship.velocity` and all external interfaces. No data
migration; low-speed behavior stays close to current. Update docs.

## Open Questions

- None blocking. The default value of `c` and the exact thrust-force tuning are
  tuning choices adjustable in config without changing the specs.
