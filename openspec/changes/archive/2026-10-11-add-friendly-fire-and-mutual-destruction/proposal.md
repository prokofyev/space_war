## Why

The current simulation treats every hit as if it were the last: `_resolve_round`
only closes the round when exactly one ship is dead, so a mutual kill leaves both
ships destroyed with the match permanently frozen. Friendly fire is silently
ignored, so a missile passes through the ship that fired it, and a player's own
two missiles never intercept each other. This change makes destruction
consequences complete and symmetric: any death scores for the survivor's
opponent, both ships can die in one exchange, and the round keeps running for a
short window so in-flight missiles can still land.

## What Changes

- **BREAKING** A ship can now be destroyed by the missile it fired, once that
  missile has left its own collision radius (friendly fire is enabled).
- **BREAKING** Missiles fired by the same player can intercept each other.
- A destroyed ship always awards one point to the opposing player, regardless of
  who caused the destruction (enemy missile, own missile, or a ship collision).
- A round now ends on a fixed 2-second timer that starts at the **first** death
  and does not restart when the second ship dies; controls, firing, movement, and
  missile damage all stay active during that window.
- Firing gains a per-player cooldown so missiles from the same ship do not spawn
  overlapped and annihilate each other instantly.
- `destruction_pause` is reused as the round-end window and its value changes
  from `1.0` to `2.0`; a new `fire_cooldown` constant is added.

## Capabilities

### New Capabilities
<!-- None. -->

### Modified Capabilities
- `space-war/missiles`: friendly fire after arming, same-owner interception, and
  the fire cooldown.
- `space-war/match-flow`: death by any cause scores for the opponent, mutual
  destruction is supported, and the round-end window keeps simulating.
- `space-war/configuration`: `destruction_pause` becomes the 2-second round-end
  window and `fire_cooldown` is added.

## Impact

- `space_war/world.py`: `step` must keep resolving hits during the round-end
  window instead of short-circuiting; `_fire` gains cooldown tracking; missile
  ownership filtering changes in `_resolve_missile_ship_hits` and
  `_resolve_missile_interceptions`; `_resolve_round` must score every death and
  start a single non-restarting timer.
- `space_war/entities.py`: a missile needs to record whether it has armed (left
  its owner's collision radius).
- `space_war/config.py`: `destruction_pause` default `2.0`, new `fire_cooldown`
  (recommended `0.2`).
- Tests: `tests/test_missiles.py`, `tests/test_match_flow.py`,
  `tests/test_gravity.py`, `tests/test_config.py`, `tests/test_effects.py` need
  updates for the new friendly-fire, interception, and round-window behavior.
- No new dependencies; the simulation stays headless and deterministic.
