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
alive at their start positions and SHALL end when exactly one ship is
destroyed by a missile.

#### Scenario: Round ends when a ship is destroyed

- **WHEN** a ship is destroyed by a missile
- **THEN** the round ends immediately

#### Scenario: New round begins automatically

- **WHEN** a round has ended
- **THEN** both ships respawn at their start positions, active missiles are
  cleared, and a new round begins without requiring the players to restart the
  application

### Requirement: Scoring

Each player's score SHALL persist across rounds within a match. The player who
survived a round SHALL be awarded exactly one point, and the destroyed player
SHALL not be awarded a point for that round.

#### Scenario: Surviving player is awarded a point

- **WHEN** a player destroys the opposing ship with a missile
- **THEN** the firing player's score increases by exactly one and the opposing
  score is unchanged

#### Scenario: Scores accumulate across rounds

- **WHEN** multiple rounds have been played in one session
- **THEN** each player's displayed score equals the number of rounds that
  player has won in the session

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
