## Why

Ships are currently drawn as a flat coloured ring with a single white direction
line (see `space_war/render.py`), so their rotation is barely readable, they
have no depth, and nothing happens visually when a ship is destroyed - the
round simply restarts. The arcade reads as a prototype rather than a game.

## What Changes

- Render ships procedurally with a clear silhouette that makes orientation
  obvious (nose, fins, exhaust nozzle), added depth (top highlight, bottom
  shade), and a soft glow halo, drawn by pre-rendering one sprite and rotating
  it per frame.
- Add an animated thrust flame from the ship's nozzle while the thrust key is
  held.
- Add a light trail behind missiles.
- Add a ship explosion with debris that flies outward from the destroyed ship's
  position when a missile kills it.
- Delay round restart by a short, configurable destruction pause (~1.0 s) so the
  explosion and debris are visible before both ships respawn; the pause is a
  pure-timing change to round flow and does not alter scoring.
- Keep all of the above strictly visual: debris and glow never collide, never
  deal damage, and never affect movement, ammunition, scoring, or hit detection.

## Capabilities

### New Capabilities
- `space-war/visuals`: procedural ship rendering (readable orientation, depth,
  glow halo, thrust flame), missile trails, and the ship destruction explosion
  with debris. Purely presentational.

### Modified Capabilities
- `space-war/match-flow`: the round-end behavior now includes a short
  destruction pause before the automatic respawn, so the explosion is visible.

## Impact

- `space_war/render.py` gains sprite-based drawing, glow, flame, trails, and
  explosion particles; a new `space_war/sprites.py` builds the ship sprite and
  debris procedurally.
- `space_war/world.py` gains a configurable round-end delay and a signal that a
  ship was destroyed so the visual layer can spawn debris; scoring and physics
  are unchanged.
- `space_war/config.py` gains visual parameters (glow, flame, trail, debris,
  destruction pause duration).
- Tests: new headless render/sprite tests and updated round-timing tests.
