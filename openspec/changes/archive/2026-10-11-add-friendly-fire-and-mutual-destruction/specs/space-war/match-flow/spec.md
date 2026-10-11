## MODIFIED Requirements

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
