## MODIFIED Requirements

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

## ADDED Requirements

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
