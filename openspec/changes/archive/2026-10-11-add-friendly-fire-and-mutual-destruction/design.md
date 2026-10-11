## Context

See proposal.md for motivation. The current `World.step` is a single-phase
loop: while `round_active` it applies controls, advances bodies, resolves
ship-ship, missile-expiry, missile-ship, and missile-missile collisions, then
runs `_resolve_round`. Once a ship dies, `_resolve_round` sets
`round_active = False`, and every later `step` short-circuits into a
"pause" branch that only advances bodies and wraps them. Two consequences
follow: missile damage stops the instant the round is flagged inactive, and a
second death (or a mutual kill) can never be observed by `_resolve_round`.

Two collision routines currently filter by owner. `_resolve_missile_ship_hits`
skips `i == missile.owner` and skips dead ships; `_resolve_missile_interceptions`
skips pairs with the same owner. Missiles spawn exactly at `ship.position`, and
the hit test uses `missile_radius + ship_radius`, so removing the owner filter
naively makes every shot detonate on its own ship.

## Goals / Non-Goals

**Goals:**
- Let a ship die to a missile it fired, so friendly fire works once the missile
  has cleared the firing ship's collision radius.
- Let same-player missiles intercept each other, with a fire cooldown so a
  rapid double-shot does not spawn overlapped missiles.
- Score every destruction for the opponent at the moment it happens, including
  mutual destruction.
- Keep the round fully simulated for a fixed 2-second window after the first
  death, so late hits still count.

**Non-Goals:**
- Changing ship-vs-ship collisions or gravity behavior.
- Adding a between-round "everyone is dead" special case beyond the timer.
- Persisting cooldown or arming state across rounds.

## Decisions

**Arming by distance cleared, not by a timer.** A missile tracks a boolean (or
the equivalent) that becomes true the first time its distance from its firing
ship exceeds `ship_radius + missile_radius`. Rationale: at the default values
this clears in roughly 58 ms of straight flight, it is frame-rate independent,
it needs no new config constant, and it exactly matches the geometry of the hit
test. Alternative considered: a `missile_self_arm_delay` in seconds. Rejected
because it is a second, redundant notion of "clear" that can disagree with the
collision radius if `ship_radius` or `missile_radius` change.

**Fire cooldown enforced in `_fire`.** Each player gets an accumulated cooldown
timer, decremented by controls update, and a shot is refused while it is
positive. Rationale: without it, two shots from a stationary ship fly in
lockstep a constant `missile_speed * dt` apart (measured 5.167 px at 120 FPS
against an 8 px interception threshold), so they annihilate instantly. A
`fire_cooldown` of `0.2 s` gives roughly 124 px of separation. Alternative
considered: an arming rule for missiles against each other too. Rejected because
the cooldown also prevents the more visible problem of two missiles occupying
almost the same point, and keeps the intent ("shots are spaced") explicit.

**Single round-end timer, not per-death.** `_resolve_round` scores the
opponent of every ship that is dead and not yet scored this round, then starts
the window only if it is not already running. A per-round `scored` mask (or
equivalent) prevents double-scoring a ship that stays dead across frames.
Rationale: the timer must not restart when the second ship dies, and re-running
`step` after the first death must not award the same point again. Alternative
considered: end the round on the first death and ignore later hits. Rejected
because it contradicts the requested behavior.

**Damage keeps resolving inside the window.** The window is a distinct state
from the old passive pause: bodies advance, controls and firing still apply,
and missile-ship and missile-missile collisions still run. Only the round-close
action is deferred until the timer expires. `reset_round` still clears all
missiles, matching the existing "active missiles are cleared" requirement.

**Config reuse.** `destruction_pause` keeps its name and meaning (the delay
from destruction to respawn) but its default becomes `2.0`; `fire_cooldown` is
added. Rationale: no schema churn for existing tests beyond values, and the
window duration is exactly what `destruction_pause` already described.

## Risks / Trade-offs

- [Friendly fire could make a stationary player kill themselves] -> The arming
  distance means a shot always clears its own ship first; only a returning or
  gravity-curved missile can hit its owner.
- [A long round-end window lets a losing player keep scoring] -> Intended per
  the requested rules; the window is short (2 s) and fixed, and it gives the
  already-in-flight missile its chance.
- [Same-player interception could be exploited to waste ammo] -> Interception
  costs both missiles and the player's own magazine, so it is self-limiting.
- [Scoring a dead ship more than once across frames] -> Track which ships have
  already been scored in the current round and only award each once.
- [Cooldown state leaking across rounds] -> Reset cooldown timers in
  `reset_round` alongside ammo and recharge.

## Migration Plan

1. Add missile arming state to the entity and set it in the collision routine.
2. Add `fire_cooldown` to the config and cooldown state to `World`, reset on
   round start.
3. Rework `step` so the round-end window keeps simulating and resolving damage.
4. Change `_resolve_round` to score all newly dead ships and start the timer
   once.
5. Update tests for friendly fire, same-owner interception, mutual destruction,
   and the new window timing. Rollback is a revert of these files; no data
   migration is involved.

## Open Questions

None.
