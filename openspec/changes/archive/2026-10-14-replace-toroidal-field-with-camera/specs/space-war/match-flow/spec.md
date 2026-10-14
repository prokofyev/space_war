## MODIFIED Requirements

### Requirement: Fullscreen display

The game SHALL run in fullscreen mode, occupying the entire selected display
with no window frame or decorations. The display SHALL show the current view of
the infinite world through a camera that frames both ships, rather than a finite
playfield sized to the display resolution.

#### Scenario: Launches in fullscreen

- **WHEN** the game starts
- **THEN** the display covers the entire screen in fullscreen mode with no
  window borders

#### Scenario: Playfield adapts to the display resolution

- **WHEN** the game runs on a display whose resolution differs from another
  display or a previous run
- **THEN** the camera frames both ships within the current display resolution
  and the simulation is unaffected by the resolution

### Requirement: Round lifecycle and restart

A match SHALL consist of successive rounds. A round SHALL begin with both ships
alive at their start positions. When a ship is destroyed the round SHALL NOT end
immediately: it SHALL enter a fixed round-end window of a configured duration
that starts at the first destruction and SHALL NOT restart or extend when any
later ship is destroyed during that window. Throughout the window the round
SHALL keep simulating at full gameplay strength: controls, firing, movement,
gravity, and missile damage all remain active, and ships may still be destroyed.
Only when the window elapses SHALL the next round begin. This allows a missile
already in flight, or a shot fired during the window, to destroy the other ship
and to award its opponent a point.

#### Scenario: Round ends when a ship is destroyed

- **WHEN** a ship is destroyed by a missile
- **THEN** the round enters the round-end window
- **AND** the round closes and the next round begins only after that window
  elapses

#### Scenario: Surviving objects keep moving during the pause

- **WHEN** a ship has been destroyed and the round is in the round-end window
- **THEN** ships respond to controls, players can fire, and active missiles
  continue to fly and expire by lifetime

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
  keep moving, and missiles still destroy ships

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
