## 1. Bundle the artwork

- [x] 1.1 Create `space_war/assets/ships/` and move the four root images into it
  with clean names (`blue_engines_off.jpeg`, `blue_engines_on.jpeg`,
  `red_engines_off.jpeg`, `red_engines_on.jpeg`); confirm they are gone from the
  project root and tracked by git.
- [x] 1.2 Add a ship sprite scale (and/or asset directory) value to
  `space_war/config.py` with a sensible default; verify `GameConfig()`
  constructs and `tests/test_config.py` passes.

## 2. Image-backed ship sprites

- [x] 2.1 Replace the procedural `build_ship_surface` with a loader that reads
  the player's image from the bundled assets directory, keying out the black
  background (`set_colorkey((0, 0, 0))`), scaling to the ship's on-screen size,
  and returning an SRCALPHA, non-empty surface at least `ship_radius` in size.
- [x] 2.2 Pre-rotate the loaded image so its nose points along +x, matching the
  simulation angle convention, and verify the sprite rotates visibly across
  angles.
- [x] 2.3 Extend `SpriteCache` to hold, per player, an idle ship sprite and a
  thrusting ship sprite (plus the existing glow), loading both engine variants;
  verify the two players' sprites differ.

## 3. Render engine state instead of a flame

- [x] 3.1 Update `Renderer._draw_ship` to select the thrusting sprite while the
  player's thrust input is held and the idle sprite otherwise, and remove the
  `effects.draw_flame` call.
- [x] 3.2 Confirm the ship is drawn as a cut-out (background not covering the
  playfield) and that the glow halo still renders beneath the ship.

## 4. Update tests and docs

- [x] 4.1 Update `tests/test_sprites.py` for image-backed sprites: SRCALPHA and
  bounding size, distinct per-player artwork, and cached idle/thrusting variants.
- [x] 4.2 Update `tests/test_effects.py` so the flame-thrusting test asserts the
  engines-on frame differs from the engines-off frame while thrusting instead of
  calling the procedural flame.
- [x] 4.3 Run `uv run pytest -q` until green, and update `README.md` if it
  describes the ship visuals.
