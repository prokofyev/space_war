## Context

See `proposal.md` - Why. The simulation is in `space_war/world.py` and is
window-free and unit-tested. Motion is relativistic: `space_war/relativity.py`
provides `momentum`, `velocity_from_momentum`, `gamma`, `energy`. Force is
applied as `p += F * dt` (see `World._thrust`). The playfield is a torus;
`World.distance` and the module-level `toroidal_delta` give the shortest wrapped
distance, already used for collisions. Bodies are `Ship` and `Missile` in
`space_war/entities.py`. There is no gravity today, and `GameConfig` has
`ship_mass`, `missile_*`, `speed_of_light`.

The behavior contract is the new `space-war/gravity` capability plus MODIFIED
requirements in `space-war/ship-movement`, `space-war/missiles`, and
`space-war/configuration`.

## Goals / Non-Goals

**Goals:**

- Make every body attract every other body with an inverse-square force.
- Compute the force on the toroidal field (attraction through edges).
- Apply it through the existing relativistic momentum model so `c` is never
  reached.
- Keep it deterministic, frame-rate independent, and headless testable.

**Non-Goals:**

- A central star or fixed gravity well (explicitly out of scope for now).
- Orbital-mechanics accuracy (no general relativity, no precession goals).
- General-relativistic light bending or rendering effects.
- Making debris or effects gravitationally active (they remain visual only).

## Decisions

**Pairwise inverse-square force.** For bodies i, j with masses m_i, m_j and
shortest toroidal separation r: `F = G * m_i * m_j / r^2`, directed from i toward
j. The net force on each body is the vector sum over all other bodies. Gravity
is applied as a momentum change `p += F_net * dt` (matching `_thrust`), then
velocity is derived via `velocity_from_momentum`. Alternative: apply an
acceleration to velocity directly - rejected because it would not respect the
relativistic mass growth and could push a body toward `c`.

**Toroidal separation via the existing helper.** Reuse the same shortest-delta
logic as collisions, so a body near the right edge is attracted to one near the
left edge across the seam, not across the full field. Alternative: Euclidean
distance - rejected; it would be inconsistent with wrapping movement.

**Softening to avoid singularities.** When two bodies coincide (or the modular
distance is ~0), the `1/r^2` force diverges. Clamp `r` to a small minimum
(`r = max(r, eps)`), so the force stays finite. This also keeps a ship and a
missile fired from it from producing an infinity at spawn. Alternative: skip
pairs below a cutoff - rejected because a hard cutoff is discontinuous; a soft
floor is smoother and simpler.

**All bodies attract all bodies.** Ships and missiles are both sources and
targets. Debris is not a simulation body, so it is naturally excluded.
Alternative: only ships as sources - the user explicitly chose "everything
attracts everything".

**Frame-rate independence.** `p += F * dt` is integrated per `dt`; for large
`dt` or close approaches, sub-step the gravity update (reusing the same
sub-stepping threshold as the thrust/momentum integration) so results do not
depend on frame rate. Alternative: single big step - rejected near strong
fields.

**Masses and the gravitational constant.** Reuse `ship_mass` as the ships'
gravitational mass; add a missile mass and one `gravitational_constant` (`G`) to
`GameConfig`, all configurable. Magnitudes are tuning values; the specs only
require that they are configurable and that heavier bodies attract more.

**Closes the distance/velocity assumptions.** Because gravity bends paths, the
"coasting is a straight line" and "missile flies in a straight line" wordings
are updated in the MODIFIED requirements; the straight-line behavior still holds
when no other body is near.

## Risks / Trade-offs

- [Singularity / NaN] Coincident or near-coincident bodies -> clamp `r` with a
  small epsilon; a test asserts finite values.
- [Instability at high speed] Strong close passes integrated in one step can be
  inaccurate -> sub-step gravity when `dt` is large or the pair is close.
- [Runaway mutual attraction] Two ships can be slung together and gain speed ->
  the relativistic limit caps speed at `c`, and G is a tunable tuning knob.
- [O(N^2) cost] Every pair attracts every pair -> fine for the small body count
  here (2 ships plus a few missiles); revisit only if counts grow.
- [Feel] Gravity could dominate and make aiming frustrating -> default G modest
  and configurable; document the value.

## Migration Plan

Additive physics change. Add `gravitational_constant` and a missile mass to
config; add a gravity step to `World.step`; reuse existing helpers. No data
migration. Straight-line behavior is preserved when far from other bodies.

## Open Questions

- None blocking. The default `G` and missile mass are tuning choices adjustable
  in config without changing the specs.
