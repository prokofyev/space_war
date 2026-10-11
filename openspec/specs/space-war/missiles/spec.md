# missiles Specification

## Purpose

Defines how each player fires and manages missiles: the Shift firing control,
the limited starting magazine with slow replenishment, missiles that fly a
bounded time under gravity before self-destructing, and the two ways a missile
can be removed by hitting another object (it destroys an enemy ship, or it
intercepts another missile).

## Requirements

### Requirement: Missile firing control

Each player SHALL fire a missile by pressing their own Shift key when their
magazine contains at least one missile and their firing cooldown has elapsed.
Firing SHALL be possible while a round is in progress, including during the
round-end window, and SHALL NOT fire when the magazine is empty or while the
cooldown is still running.

#### Scenario: Player fires an available missile

- **WHEN** a round is in progress and a player with missiles in the magazine
  presses the fire key and is not on cooldown
- **THEN** one missile spawns at that ship's position, traveling along the
  ship's facing direction, and one missile is removed from that player's
  magazine

#### Scenario: Firing with an empty magazine does nothing

- **WHEN** a player whose magazine contains no missiles presses the fire key
- **THEN** no missile is created and the magazine stays empty

#### Scenario: Missile inherits ship velocity contribution

- **WHEN** a missile is fired from a moving ship
- **THEN** the missile's initial velocity combines the ship's velocity with the
  missile's launch speed along the facing direction

#### Scenario: Firing respects the cooldown

- **WHEN** a player presses the fire key again before the configured firing
  cooldown has elapsed since their previous shot
- **THEN** no second missile is created and the magazine is not charged

### Requirement: Missile ammunition and replenishment

Each player SHALL start a match with a magazine capacity of three missiles and
SHALL be limited to that capacity. The magazine SHALL replenish automatically
over time while a round is in progress, one missile per configured replenish
interval, and SHALL never exceed the capacity.

#### Scenario: Match starts with three missiles per player

- **WHEN** a new match begins
- **THEN** each player has exactly three missiles available

#### Scenario: Replenishment restores a fired missile

- **WHEN** a player has fewer than the maximum missiles and a round is in
  progress
- **THEN** after the configured replenish interval elapses the player gains one
  missile
- **AND** the magazine never exceeds the maximum of three

#### Scenario: Replenishment does not exceed capacity

- **WHEN** a player already has the maximum number of missiles
- **THEN** elapsed replenish time does not add any further missiles

### Requirement: Missile flight lifetime and self-destruct

A missile SHALL fly under gravity along with any other bodies, and SHALL
self-destruct once it has been in flight for a configured maximum lifetime
measured in time, without harming either ship. Its trajectory is no longer
strictly a straight line, because gravitational attraction from other bodies
bends its course. Its survivable distance is therefore whatever distance it
covers during that time.

#### Scenario: Missile expires in open space

- **WHEN** a missile's flight time reaches the configured maximum lifetime
  without hitting anything
- **THEN** the missile is removed from play
- **AND** neither player's score changes

#### Scenario: Lifetime is measured in time, not distance

- **WHEN** a missile flies faster than another missile
- **THEN** both are removed after the same elapsed flight time, even though the
  faster one covered more distance

#### Scenario: Gravity bends a missile's path

- **WHEN** a missile flies near a more massive body
- **THEN** its trajectory curves toward that body instead of staying straight

#### Scenario: Missile crosses the borderless field

- **WHEN** a missile's position moves beyond an edge of the field
- **THEN** the missile re-enters from the opposite edge at the same offset and
  keeps its velocity

### Requirement: Missile destroys an enemy ship

When a missile collides with a ship, the missile SHALL be consumed and the
struck ship SHALL be destroyed. A ship that is struck by an enemy missile SHALL
award the opposing player one point. A missile SHALL only destroy the ship that
fired it once it has first left that ship's collision radius.

#### Scenario: Missile hits the enemy ship

- **WHEN** a missile collides with the ship of the player who did not fire it
- **THEN** the struck ship is destroyed and the firing player's score increases
  by one

#### Scenario: Missile does not hit its own ship

- **WHEN** a missile is fired by a player and has not yet left the firing
  player's ship collision radius
- **THEN** it does not destroy the firing player's own ship

### Requirement: Missile intercepts another missile

When two missiles collide, both missiles SHALL be consumed and neither SHALL
damage a ship as a result of that collision, regardless of which player fired
either missile.

#### Scenario: Opposing missiles collide

- **WHEN** two missiles from opposing players occupy overlapping positions
- **THEN** both missiles are removed from play
- **AND** neither player is destroyed or scored against because of the
  interception

#### Scenario: Same-player missiles collide

- **WHEN** two missiles fired by the same player occupy overlapping positions
- **THEN** both missiles are removed from play
- **AND** no ship is damaged and no score changes

### Requirement: Missile arming against its own ship

A missile SHALL NOT destroy the ship that fired it until it has first left that
ship's collision radius. Once the missile has left its firing ship's collision
radius it SHALL remain able to destroy that ship, so a missile that returns to
its owner can destroy it.

#### Scenario: Freshly fired missile spares its own ship

- **WHEN** a missile has just been fired and still overlaps the collision radius
  of the ship that fired it
- **THEN** the firing ship is not destroyed and the missile remains in flight

#### Scenario: Returning missile can destroy its own ship

- **WHEN** a missile that already left its firing ship's collision radius
  returns and collides with that ship
- **THEN** the ship is destroyed and the opposing player is awarded one point

### Requirement: Firing cooldown between shots

A player SHALL NOT be able to fire another missile until a configured firing
cooldown has elapsed since their previous shot, so that two missiles from the
same ship do not spawn overlapping each other.

#### Scenario: Second shot is blocked during the cooldown

- **WHEN** a player fires and then presses fire again before the cooldown
  elapses
- **THEN** only the first missile exists and the second press has no effect

#### Scenario: Shot is allowed after the cooldown elapses

- **WHEN** the configured firing cooldown has fully elapsed since the player's
  previous shot and the magazine is not empty
- **THEN** the player can fire another missile

### Requirement: Missile speed of light limit

The speed of light `c` SHALL bound missiles as well as ships. A missile's launch
velocity SHALL be the relativistic addition of the firing ship's velocity and
the missile's muzzle velocity along the facing direction, so a missile can never
reach or exceed `c`, and in flight a missile SHALL never exceed `c`.

#### Scenario: Missile launched from a fast ship stays below the limit

- **WHEN** a missile is fired from a ship moving at a large fraction of `c`
  along the firing direction
- **THEN** the missile's launch speed is the relativistic sum of the ship's
  velocity and the muzzle velocity and remains strictly below `c`

#### Scenario: Relativistic addition at low speed matches the naive sum

- **WHEN** the firing ship is slow compared to `c`
- **THEN** the missile's launch velocity is approximately the ship's velocity
  plus the muzzle velocity along the facing direction

#### Scenario: Missile in flight never exceeds the limit

- **WHEN** a missile is in flight
- **THEN** its speed stays strictly below the speed of light
