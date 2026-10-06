## Context

See `proposal.md` - Why. The repository is a bare Python 3.13 project with a
`uv`-managed `pyproject.toml`, a hello-world `main.py`, and no gameplay code,
tests, or extra dependencies. The runtime target is a single local desktop
running a fullscreen display where two people share one keyboard.

The behavior contract is fully captured by the delta specs:
`space-war/ship-movement`, `space-war/missiles`, `space-war/match-flow`, and
`space-war/configuration`. This design covers only the technical choices needed
to satisfy them.

## Goals / Non-Goals

**Goals:**

- Keep the physics/combat simulation a pure, deterministic, window-free core so
  it can be unit-tested headlessly.
- Separate simulation, rendering, and input so Pygame stays at the edges.
- Make every tunable (physics, combat, controls) live in one configuration
  module, with field size derived from the fullscreen display resolution.
- Give the frame loop a fixed-order update so wrapping, collisions, and missile
  removals are deterministic regardless of frame rate.

**Non-Goals:**

- Networking, remote play, or more than two players.
- Menus, match-to-N-wins rules, pause, or persistent high scores.
- Sound, particle systems, or sprite-driven art assets.
- Anti-cheat, replays, or save/load.

## Decisions

**Project layout: a `space_war` package with a pure `sim` core.**
Structure:

- `space_war/config.py` - constants and per-player bindings (dataclasses).
- `space_war/vector.py` - small 2D vector helpers (or use plain tuples).
- `space_war/entities.py` - `Ship` and `Missile` state dataclasses.
- `space_war/world.py` - `World` holding ships, missiles, scores, round state;
  owns `step(dt, controls)` with all update ordering.
- `space_war/input.py` - maps Pygame key state to a per-player `Controls`
  struct; the only place key codes are read.
- `space_war/render.py` - draws `World` to a Pygame surface.
- `space_war/game.py` - opens the fullscreen display, derives the field size
  from its resolution, runs the loop, and wires input → world → render.
- `main.py` - thin launcher calling `space_war.game.run()`.

Rationale: the whole contract is testable from `world.py` alone. Alternative
considered: one monolithic `main.py` - rejected because headless tests would be
awkward and physics/rendering would couple.

**Pygame behind an edge, simulation as plain math.** The simulation deals in
floats and simple objects and never imports `pygame`. Rendering consumes the
sim state. Alternative: use `pygame.math.Vector2` everywhere - rejected to
avoid a Pygame dependency in tests and to keep vectors serializable.

**Movement model: fixed acceleration along facing, no drag.** Each step:
`angle += rotation_rate * dt * direction`; if thrust held,
`velocity += unit(facing) * thrust_accel * dt`; then
`position += velocity * dt`. Because the same velocity is added to regardless of
direction, thrust aligned with velocity speeds up, opposite slows down, and
perpendicular turns the path - exactly the "accelerate or brake depending on the
angle" requirement. Alternative: apply drag/friction - rejected because the
spec requires inertia with no automatic slowing.

**Wrapping as modular arithmetic on both axes.** After integration, map each
coordinate back into `[0, width)` / `[0, height)` with modulo (or shift-by-size
for negatives), preserving offset, velocity, and facing. Applies to ships and
missiles. Drawing optionally renders a second copy near edges so wrapped objects
look continuous; that is cosmetic only and not required by the specs.

**Collision models.** Ships are circles. Ship-vs-ship uses the equal-mass
elastic formula: project both velocities onto the collision normal (unit vector
between centers), swap the normal components, and keep the tangential
components; separate the ships to remove overlap. Missile-vs-ship and
missile-vs-missile are simple circle overlap tests; on a missile/ship hit the
round ends and scores update, on missile/missile both are removed. All
collision distances use the toroidal shortcut - compute the delta and then wrap
each component to `[-size/2, size/2)` - so collisions are detected correctly
across the seamless edge.

**Update ordering per step (deterministic):** 1) apply player controls and
integrate ships; 2) wrap; 3) resolve ship-ship collisions; 4) integrate and wrap
missiles, decrement missile lifetimes and remove expired ones; 5) resolve
missile-ship hits; 6) resolve missile-missile interceptions; 7) if a ship died,
award the point and reset the round. This order prevents a missile removed for
expiry from still hitting, and prevents double-scoring within one frame.

**Input and controls model.** Each frame `input.py` produces a `Controls`
object per player (`thrust: bool`, `rotate: -1|0|1`, `fire: bool`). `fire` is
edge-triggered (fires once per press) while `thrust`/`rotate` are level-triggered
(held keys). Alternative: fire on key-held repeat - rejected to avoid dumping
the magazine on one hold.

**Ammunition model.** Each player has a float `recharge` accumulator that
increases by `dt`; when it reaches `replenish_interval` and the magazine is below
capacity, add one missile and subtract the interval. Reset magazine and
accumulator at round start. Alternative: integer-frame cooldown - rejected
because frame-rate independence is required.

**Missiles: lifetime-bounded straight flight.** A missile stores remaining
lifetime (`< range> / <speed>`) and self-destructs when it reaches zero. Range is
configurable, satisfying "flies some distance then explodes from time".

**Configuration as dataclass constants.** `config.py` exposes a `GameConfig`
dataclass with ship radius/mass/rotation/thrust, missile speed, radius, range,
ammo start/max, replenish interval, start positions/facings, plus a per-player
binding map. Field width/height are not hardcoded: `game.py` reads the current
fullscreen display resolution and passes those dimensions into the `World`.
`GameConfig` is injectable so tests can use tiny fields and short ranges without
changing logic.

**Fullscreen display.** `game.py` opens the display with
`pygame.display.set_mode((0, 0), pygame.FULLSCREEN)` so it fills the native
resolution, and derives the playfield size from the returned surface size. Since
a fullscreen display has no title-bar close button, Escape is the quit control.
Alternative: a fixed-size window sized to the desktop - rejected because the
request is fullscreen. Alternative: exclusive/scaled fullscreen with a
letterboxed fixed playfield - rejected so the whole screen stays usable play
area.

**Testing approach.** `pytest` (add as a dev dependency) on `world.py` with a
tiny config: rotation, thrust acceleration/braking/deflection, wrap on both
axes and corners, equal-mass collision momentum/energy conservation, missile
spawn/ammo, replenishment capped at max, expiry, missile-ship hit scoring and
reset, and missile-missile interception. No Pygame window is opened in tests.

## Risks / Trade-offs

- [Tunneling] Fast missiles/ships could skip through each other between frames →
  use a swept/segment check against the toroidal delta, or substep when the
  relative displacement per frame exceeds the sum of radii.
- [Collision edge cases at wrap seams] Naive distance checks break at edges →
  centralize the toroidal delta helper and use it everywhere distances are
  compared.
- [Equal-mass collision still leaves overlap] Two ships can re-collide next
  frame → after swapping normal components, push both ships apart along the
  normal to just touching.
- [Frame-rate dependence] Per-frame counting would break behavior → drive all
  rates by `dt`, clamp very large `dt` after display stalls, and cover with
  frame-rate tests.
- [Fullscreen resolution variance] Playfield size and start positions can differ
  across displays → derive width/height from the display surface at runtime and
  express start positions/facings relative to those dimensions rather than as
  absolute pixels.
- [No window controls in fullscreen] There is no title-bar close button →
  provide an Escape quit key (and still handle the Pygame quit event).
- [Round reset timing] Scoring/reset in the same frame as the hit can double
  process → single ordered `step` that resolves the round once per step.
- [Sim/visual coordinate drift] Rendering a seamless world from a single copy
  can look discontinuous at the seam → optional second draw pass near edges;
  cosmetic and independent of the wrapped simulation.

## Migration Plan

Greenfield addition: add the `space_war` package, repoint `main.py` at the game
launcher, add `pygame` to runtime dependencies and `pytest` to dev
dependencies. No data migration and no rollback concerns beyond reverting the
new files.

## Open Questions

- None blocking. Deferred, spec-neutral tuning choices left to implementation:
  start positions/facings and the numeric values of rotation rate, thrust
  acceleration, missile speed/range, and replenish interval - all live in
  `GameConfig` and can be tuned freely without changing the specs. The playfield
  size is not an open question: it follows the fullscreen display resolution.
