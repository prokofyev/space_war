# missiles Specification

## Purpose

Defines how each player fires and manages missiles: the Shift firing control,
the limited starting magazine with slow replenishment, missiles that fly a
bounded distance before self-destructing, and the two ways a missile can be
removed by hitting another object (it destroys an enemy ship, or it intercepts
another missile).

## Requirements

### Requirement: Missile firing control

Each player SHALL fire a missile by pressing their own Shift key when their
magazine contains at least one missile. Firing SHALL only be possible while a
round is in progress, and SHALL NOT fire when the magazine is empty.

#### Scenario: Player fires an available missile

- **WHEN** a round is in progress and a player with missiles in the magazine
  presses the fire key
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

A missile SHALL travel in a straight line at constant velocity and SHALL
self-destruct once it has been in flight for a configured maximum lifetime
measured in time, without harming either ship. Its survivable distance is
therefore whatever distance it covers during that time at its own speed.

#### Scenario: Missile expires in open space

- **WHEN** a missile's flight time reaches the configured maximum lifetime
  without hitting anything
- **THEN** the missile is removed from play
- **AND** neither player's score changes

#### Scenario: Lifetime is measured in time, not distance

- **WHEN** a missile flies faster than another missile
- **THEN** both are removed after the same elapsed flight time, even though the
  faster one covered more distance

#### Scenario: Missile crosses the borderless field

- **WHEN** a missile's position moves beyond an edge of the field
- **THEN** the missile re-enters from the opposite edge at the same offset and
  keeps its velocity

### Requirement: Missile destroys an enemy ship

When a missile collides with a ship controlled by the other player, the missile
SHALL be consumed, the struck ship SHALL be destroyed, and the opposing player
SHALL be awarded one point for the round.

#### Scenario: Missile hits the enemy ship

- **WHEN** a missile collides with the ship of the player who did not fire it
- **THEN** the struck ship is destroyed and the firing player's score increases
  by one
- **AND** the round ends and a new round begins

#### Scenario: Missile does not hit its own ship

- **WHEN** a missile is fired by a player
- **THEN** it does not collide with or destroy the firing player's own ship

### Requirement: Missile intercepts another missile

When two missiles fired by opposing players collide, both missiles SHALL be
consumed and neither SHALL damage a ship as a result of that collision.

#### Scenario: Opposing missiles collide

- **WHEN** two missiles from opposing players occupy overlapping positions
- **THEN** both missiles are removed from play
- **AND** neither player is destroyed or scored against because of the
  interception

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
