## Why

Ships are currently drawn as procedural polygons, which look crude compared to
the rest of the presentation. The author has provided finished artwork for both
players (blue and red), each with an "engines off" and an "engines on" variant,
so the game can render recognizable, hand-made ships and show thrust with a lit
engine image instead of a procedural flame.

## What Changes

- Move the four provided ship images out of the project root into a dedicated
  bundled assets folder inside the package.
- Render each ship from its player's image instead of the procedural torus
  shape, keeping the shipped orientation readable and tied to the simulation
  angle.
- Remove the black image background so ships are drawn as cut-outs rather than
  opaque squares.
- Replace the procedural thrust flame with the "engines on" image variant:
  a ship shows its "engines on" sprite while the thrust key is held and its
  "engines off" sprite otherwise.
- Keep the soft glow halo and the two players visually distinct (blue vs red).

## Capabilities

### New Capabilities
- `space-war/assets`: ship artwork is stored as bundled image files, loaded and
  mapped to each player and to the idle/thrusting states, with the image
  background made transparent.

### Modified Capabilities
- `space-war/visuals`: ships are now rendered from authored images (not
  procedural shapes), and the thrust flame requirement becomes an
  engines-on/engines-off image swap.

## Impact

- `space_war/assets/ships/` (new) gains the four moved image files;
  the four files are removed from the project root.
- `space_war/sprites.py` loads the images, removes the background, scales and
  caches both engine states per player.
- `space_war/render.py` picks the engines-on sprite while thrusting and drops
  the procedural flame call.
- `space_war/config.py` gains a ship sprite scale / asset location value.
- Tests: `tests/test_sprites.py` updated for image-based sprites and the
  engine on/off variants; `tests/test_effects.py` updated because the flame is
  now a sprite swap.
- `README.md` updated if it describes the ship visuals.
