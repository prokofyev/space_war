## Why

The playfield currently has no forces other than player thrust: a coasting ship
drifts forever in a straight line and a fired missile never curves. Adding an
omnipresent gravitation between all bodies turns the arena into a dynamic
environment where trajectories bend, aiming requires leading the shot, and
motion itself becomes a hazard to manage - the core appeal of gravity-based
space combat.

## What Changes

- Introduce a universal gravitational attraction: every body attracts every
  other body, acting on ships and missiles alike.
- Model it as a pairwise force between two bodies proportional to the product
  of their (relativistic) masses and inversely proportional to the square of the
  distance between them, applied over time by changing each body's momentum
  (consistent with the existing relativistic force model).
- Compute distances across the borderless playfield using the shortest
  toroidal distance, so gravity acts through the edges exactly like movement
  and collisions already do.
- Give missiles, ships, and their gravity-relevant masses configuration values,
  and make the gravitational constant a tunable gameplay constant.
- Update the affected movement/missile requirements: coasting is no longer
  strictly straight-line, and a missile no longer flies in a perfectly straight
  line, because gravity now bends their paths.

## Capabilities

### New Capabilities
- `space-war/gravity`: mutual gravitational attraction between all bodies
  (ships and missiles) computed on the toroidal field, applied through the
  relativistic momentum model.

### Modified Capabilities
- `space-war/ship-movement`: thrust-free motion is now affected by gravity; a
  coasting ship's path curves under the attraction of other bodies instead of
  being a straight line.
- `space-war/missiles`: an in-flight missile no longer travels in a strictly
  straight line; gravity bends its trajectory.
- `space-war/configuration`: add the gravitational constant and per-object
  masses used by gravity.

## Impact

- `space_war/config.py` gains a gravitational constant and any per-object mass
  values needed for gravity.
- `space_war/world.py` gains a gravity step that changes each body's momentum
  using the toroidal distance helper already used for collisions.
- `space_war/entities.py` may need a gravitational mass/charge per body.
- Tests: new gravity tests (attraction direction, inverse-square falloff,
  toroidal-through-edge attraction, all-bodies attract all); movement and
  missile tests updated to account for curved paths.
- `README.md` updated to describe gravity.
