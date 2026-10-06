## Context

See `proposal.md` - Why. Current rendering in `space_war/render.py` draws each
ship inline every frame as `circle(color)` + `circle(background)` + a white
facing line, and missiles as plain circles. The simulation (`space_war/world.py`)
is window-free and unchanged by presentation. Field size follows the fullscreen
display resolution.

The behavior contract is the `space-war/visuals` delta plus the MODIFIED
round-lifecycle requirement in `space-war/match-flow`.

## Goals / Non-Goals

**Goals:**

- Make ship orientation unmistakable and give ships depth, a glow halo, a thrust
  flame, missile trails, and a debris explosion.
- Keep presentation fully decoupled from physics: debris/glow/trails never touch
  collision, damage, ammo, or scoring.
- Keep rendering testable headlessly (no real window).

**Non-Goals:**

- Art-asset pipelines, sprite sheets, or external image files.
- Particle physics in the simulation; debris is a render-layer concern only.
- Changing ship movement, collision, missile, or scoring rules.
- Menus, HUD redesign, or sound.

## Decisions

**Pre-render the ship sprite once, rotate per frame.** Build a single
anti-aliased ship surface (nose along +x) per player colour at 4x resolution and
`smoothscale` down, then draw it with `pygame.transform.rotozoom(sprite,
-degrees(angle), 1.0)`. Rationale: rotating whole body markers (nose, fins,
nozzle) makes orientation read correctly, unlike the current rotation-invariant
ring. Alternative: transform per-frame drawing of each polygon - rejected as
more expensive and harder to shade consistently.

**Procedural sprite, no assets.** `sprites.build_ship_surface(config, player)`
draws the body with layered polygons: base fill, top highlight, bottom shade,
fins, a nozzle, and a cockpit accent; `build_glow_surface(...)` produces a soft
radial halo. Rationale: no new dependencies, deterministic, testable. Alternative:
imagegen bitmaps - rejected for this scope (asset management, lighting
consistency, and rotation blur).

**Debris as a render-layer particle list.** The simulation raises a signal when a
ship is destroyed (a per-frame `destroyed_events` list carrying the ship's index,
position, angle, and velocity). `render.py` owns the debris list: on a
destruction event it spawns N pieces with randomised outward directions and
speeds, and adds the destroyed ship's velocity to each piece so the whole cloud
inherits the ship's momentum; each step the pieces decelerate and fade and are
dropped after a lifetime, updated with the same `dt` as the world so they keep
moving during the pause. Rationale: satisfies "purely visual" without polluting
the sim. Alternative: model debris in `World` - rejected because it would add
non-gameplay state to the determinism-tested core.

**Round-end pause lives in the simulation, explosion lives in render.** The
pause is gameplay timing (it delays respawn), so `World` gains
`round_pause_remaining` and a `destruction_pause` config value: on destruction it
stops scoring, records the destroyed ship, enters a paused state, and calls
`reset_round()` only when the timer elapses. The pause delays only the respawn;
the rest of the world keeps advancing during it - surviving ships keep their
momentum and in-flight missiles keep flying, wrapping, and expiring. The
explosion art is driven by the render layer observing the destruction, which is
exactly the window during which the pause runs. Alternative: pause only in
`game.py` - rejected because tests assert round timing in the window-free core.
Alternative: fully freeze the world during the pause - rejected because the
surviving objects should stay visibly alive while the debris flies.

**Where the destruction signal comes from.** `World` exposes the newly
destroyed ship(s) for the frame (e.g. `last_destroyed: list[tuple[int, pos,
angle]]` cleared at the start of each `step`). `game.py`/`render.py` consume it
once to spawn debris and clear the list. Rationale: single, explicit handoff;
keeps `World` free of particle state.

**Config additions.** `destruction_pause` (~1.0 s), `debris_count`,
`debris_speed`, `debris_lifetime`, `debris_fade`, `flame_length`,
`flame_animation_speed`, `trail_length`, `trail_points`, and glow radius/alpha.
All optional with defaults so existing configs keep working.

## Risks / Trade-offs

- [Sprite blur on rotation] Rotated sprites can look soft at extreme angles ->
  pre-render at 4x and downscale, and keep the silhouette chunky.
- [Debris in the render layer desyncs from the sim] Debris could outlive its
  round -> clear all debris on any round reset and cap particle count.
- [Pause changes round timing and could break existing tests] The old behavior
  respawns in the same step -> update round-timing tests to advance past the
  pause and assert scoring is unchanged; default the pause in config.
- [Frame-rate dependence of particle fade] Fade/slowdown must use `dt`, not
  frames -> drive the particle update with the same `dt` as the world.
- [Per-frame allocations] Building rotated surfaces each frame allocates ->
  pre-render base sprites once and cache them per colour.

## Migration Plan

Additive presentation change plus one timing tweak. Ship sprite and particles
add ~one module; `render.py` and `world.py` change in place; `config.py` gains
optional fields with defaults. No data migration. Old visuals are fully
replaced.

## Open Questions

- None blocking. Deferred, spec-neutral tuning: exact debris count/speed,
  flame length, glow radius, and trail length - all live in config.
