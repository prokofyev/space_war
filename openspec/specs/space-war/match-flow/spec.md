# match-flow Specification

## Purpose

Defines the overall gameplay loop: the round lifecycle, per-player scoring, the
respawn/restart that follows a ship's destruction, and the top-level
responsibilities of running the fullscreen display, rendering, and reading
player input.

## Requirements

### Requirement: Two-player shared-keyboard session

The game SHALL run on one machine hosting exactly two players who share one
keyboard, each with independent control bindings, and SHALL render the current
round state (ships, missiles, and scores) each frame.

#### Scenario: Both players control their own ship

- **WHEN** a player presses their own movement, rotation, or fire keys
- **THEN** only that player's ship or missiles respond, and the other player's
  ship is unaffected

#### Scenario: Game state is displayed

- **WHEN** the game is running
- **THEN** the display continuously renders both ships, all active missiles, and
  both players' current scores

### Requirement: Fullscreen display

The game SHALL run in fullscreen mode, occupying the entire selected display
with no window frame or decorations, and the playfield SHALL size itself to the
full display resolution so the whole screen is usable play area.

#### Scenario: Launches in fullscreen

- **WHEN** the game starts
- **THEN** the display covers the entire screen in fullscreen mode with no
  window borders
- **AND** the playfield spans the full display resolution

#### Scenario: Playfield adapts to the display resolution

- **WHEN** the game runs on a display whose resolution differs from another
  display or a previous run
- **THEN** the playfield dimensions and edge wrapping use the current display
  resolution

### Requirement: Round lifecycle and restart

A match SHALL consist of successive rounds. A round SHALL begin with both ships
alive at their start positions. When a ship is destroyed the round SHALL NOT end
immediately: it SHALL enter a fixed round-end window of a configured duration
that starts at the first destruction and SHALL NOT restart or extend when any
later ship is destroyed during that window. Throughout the window the round
SHALL keep simulating at full gameplay strength: controls, firing, movement,
gravity, edge wrapping, and missile damage all remain active, and ships may
still be destroyed. Only when the window elapses SHALL the next round begin.
This allows a missile already in flight, or a shot fired during the window, to
destroy the other ship and to award its opponent a point.

#### Scenario: Round ends when a ship is destroyed

- **WHEN** a ship is destroyed by a missile
- **THEN** the round enters the round-end window
- **AND** the round closes and the next round begins only after that window
  elapses

#### Scenario: Surviving objects keep moving during the pause

- **WHEN** a ship has been destroyed and the round is in the round-end window
- **THEN** ships respond to controls, players can fire, and active missiles
  continue to fly, wrap at the field edges, and expire by lifetime

#### Scenario: Destruction pause precedes respawn

- **WHEN** a ship has been destroyed
- **THEN** both ships respawn only after the configured round-end window has
  elapsed

#### Scenario: First destruction starts the round-end window

- **WHEN** a ship is destroyed
- **THEN** the round enters the round-end window and starts the configured timer
- **AND** the destroyed ship does not respawn until the window elapses

#### Scenario: Gameplay stays active during the window

- **WHEN** the round is in the round-end window
- **THEN** surviving ships respond to controls, players can fire, all bodies
  keep moving and wrapping, and missiles still destroy ships

#### Scenario: A second destruction does not restart the window

- **WHEN** the other ship is destroyed during an active round-end window
- **THEN** the timer is not restarted or extended, and the new round begins when
  the originally started window elapses

#### Scenario: Both ships can be destroyed in one round

- **WHEN** both ships are destroyed within one round-end window
- **THEN** neither ship respawns until the window elapses and the round closes
  normally afterwards

#### Scenario: New round begins automatically

- **WHEN** the round-end window has elapsed
- **THEN** both ships respawn at their start positions, active missiles are
  cleared, and a new round begins without requiring the players to restart the
  application

#### Scenario: Pause duration is configurable

- **WHEN** the round-end window duration is changed in the configuration
- **THEN** the delay between the first destruction and the next round changes
  accordingly

### Requirement: Scoring

Each player's score SHALL persist across rounds within a match. Whenever a ship
is destroyed, by any cause, the opposing player SHALL be awarded exactly one
point at that moment. A round in which both ships are destroyed SHALL award one
point to each player.

#### Scenario: Surviving player is awarded a point

- **WHEN** a player destroys the opposing ship with a missile
- **THEN** the firing player's score increases by exactly one and the opposing
  score is unchanged

#### Scenario: Opponent is awarded a point when a ship is destroyed

- **WHEN** a ship is destroyed by an enemy missile
- **THEN** the firing player's score increases by exactly one and the destroyed
  player's score is unchanged

#### Scenario: Either player is awarded a point for each destruction

- **WHEN** both ships are destroyed during the same round-end window
- **THEN** each player's score increases by exactly one

#### Scenario: Friendly-fire destruction scores for the opponent

- **WHEN** a missile destroys the ship that fired it
- **THEN** the opposing player's score increases by exactly one

#### Scenario: Scores accumulate across rounds

- **WHEN** multiple rounds have been played in one session
- **THEN** each player's displayed score equals the total number of ships that
  player's opponent has lost in the session

### Requirement: Respawn state is clean

When a new round begins, each ship SHALL respawn alive at its start position
with zero velocity and a defined initial facing, and each player's magazine
SHALL be reset to the starting amount.

#### Scenario: Ships reset on respawn

- **WHEN** a new round begins
- **THEN** both ships are alive at their start positions with zero velocity

#### Scenario: Ammunition resets on respawn

- **WHEN** a new round begins
- **THEN** each player's magazine is reset to the starting amount of three
  missiles

### Requirement: Application lifecycle

The application SHALL run a real-time game loop driven by frame delta time and
SHALL exit cleanly when the player quits.

#### Scenario: Motion is frame-rate independent

- **WHEN** the game runs at different frame rates
- **THEN** ship acceleration, velocity, rotation, and missile flight advance
  proportionally to elapsed time rather than per-frame counts

#### Scenario: Quitting exits the game

- **WHEN** the player presses the quit key (Escape)
- **THEN** the game loop stops and the application terminates cleanly without an
  error
