## Context

See proposal.md for motivation. Today `World` is a torus whose `width`/`height`
come from the fullscreen surface (`world_from_display`), and wrapping is threaded
through several mechanisms: `wrap_scalar`/`toroidal_delta` define distances,
`_wrap_ships`/`_wrap_missiles` teleport bodies at the edges, and gravity and
ship-ship collisions use the wrapped shortest path. `reset_round` spawns ships at
`start_positions` given as fractions of the field, and `Renderer` draws world
coordinates directly to screen with no camera.

## Goals / Non-Goals

**Goals:**
- Make the world an unbounded plane so ships never wrap or leave a finite field.
- Keep both ships framed on screen at all times with a smooth, uniform-zoom
  camera whose initial zoom derives from `initial_ship_distance`.
- Replace display-fraction start positions with a configurable world-unit
  distance.

**Non-Goals:**
- Keeping missiles on screen (only ships must stay framed).
- Capping the zoom (the camera may magnify ships when they are close).
- Parallax, rotation, or independent X/Y scaling in the camera.
- Changing gravity's law, only its distance metric.

## Decisions

**World becomes unbounded; drop `width`/`height`.** `World` no longer needs
field dimensions, and `distance` becomes the plain Euclidean norm. Delete
`wrap_scalar`, `toroidal_delta`, `_wrap_ships`, `_wrap_missiles`, and `_size`.
Gravity, ship-vs-ship separation, missile hits, and interceptions all switch to
straight-line deltas. Alternative considered: keep a large finite plane. Rejected
because the request is explicitly an infinite world and any finite size
reintroduces a boundary to design around.

**Spawn from `initial_ship_distance` centered on the origin.** Replace
`start_positions` with `initial_ship_distance`; place ship 0 at
`(-d/2, 0)` and ship 1 at `(+d/2, 0)` with facings `0` and `pi` so they face each
other. Rationale: it makes the start distance a single tunable number and keeps
the camera target simple. Alternative: keep fractions of a notional field.
Rejected because the field no longer has a size to take fractions of.

**Camera in the render layer, not the simulation.** The simulation stays
obviously unaffected by framing; the camera is a view transform. It tracks the
midpoint of the two ships and computes a target scale as
`min(viewport_w, viewport_h) * (1 - margin) / (needed_extent)`, where the needed
extent is the ships' separation plus their drawn radii. The scale is applied
uniformly to both axes and to every drawn element (ships, missiles, trails,
debris), with the midpoint mapped to the viewport center. Rationale: keeps
presentation and physics cleanly separated. Alternative: put the camera in
`World`. Rejected because the world must stay headless and view-independent.

**Smooth, uncapped zoom.** Each frame the camera moves its scale and center
toward the target with exponential smoothing driven by `dt` (a configured
`camera_smoothing` rate), so it is frame-rate independent and never snaps. There
is no upper scale cap, so when ships are close the camera magnifies them. At
startup the scale is initialized to the target for `initial_ship_distance` so
the first frame is already framed (no zoom-in animation from zero). Alternative:
hard 1:1 cap. Rejected: the user explicitly wants the ships enlarged when close.

**HUD drawn in screen space.** Scores stay on the HUD and are drawn after the
world transform, so they are unaffected by zoom.

## Risks / Trade-offs

- [World coordinates grow unbounded, hurting float precision] → Magnitudes stay
  far below meaningful precision limits for realistic match lengths; no
  mitigation needed now.
- [Zooming out far makes ships tiny and hard to see] → The framing margin leaves
  a small border; gameplay still reads because both ships remain visible, which
  is the stated goal.
- [Smooth camera could lag a fast separation and clip a ship] → Reserve a camera
  margin and use a rate fast enough to track; tests can assert the ships remain
  inside the viewport after a step.
- [Removing wrapping changes existing tests that assumed it] → Update the
  wrapping-specific tests to assert no-wrap behavior instead.
- [Camera applied to sprites needs scale-aware rotation] → Rotate, then scale by
  the camera factor, for every drawn sprite.

## Migration Plan

1. Update `GameConfig`: remove `start_positions`, add `initial_ship_distance`,
   `camera_margin`, and `camera_smoothing`.
2. Rework `World`: drop dimensions and wrapping; spawn from the distance; use
   Euclidean distances everywhere.
3. Update `game.py` to build an unbounded world and pass the surface size to the
   camera.
4. Add the camera to `render.py` and route all drawing through it.
5. Update tests: field-dimension, collisions, gravity, missiles, movement, and
   render smoke tests. Rollback is a revert of these files; no data migration.

## Open Questions

None.
