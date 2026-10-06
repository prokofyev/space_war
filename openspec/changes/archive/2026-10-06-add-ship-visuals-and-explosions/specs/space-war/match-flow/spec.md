## MODIFIED Requirements

### Requirement: Round lifecycle and restart

A match SHALL consist of successive rounds. A round SHALL begin with both ships
alive at their start positions and SHALL end when exactly one ship is
destroyed by a missile. After a ship is destroyed, the round SHALL remain in a
destruction-pause state for a short configurable duration before the next round
begins, so the destruction is visible. During the destruction pause the
remaining objects SHALL keep moving: surviving ships keep their inertia and
missiles in flight keep flying, while only respawn is delayed.

#### Scenario: Round ends when a ship is destroyed

- **WHEN** a ship is destroyed by a missile
- **THEN** the round enters the destruction pause and no further scoring happens
  during the pause

#### Scenario: Surviving objects keep moving during the pause

- **WHEN** a ship has been destroyed and the round is in the destruction pause
- **THEN** the surviving ship continues to move under its velocity and active
  missiles continue to fly, wrap at the field edges, and expire by range

#### Scenario: Destruction pause precedes respawn

- **WHEN** a ship has been destroyed
- **THEN** both ships respawn only after the configured destruction-pause
  duration has elapsed

#### Scenario: New round begins automatically

- **WHEN** the destruction pause has elapsed
- **THEN** both ships respawn at their start positions, active missiles are
  cleared, and a new round begins without requiring the players to restart the
  application

#### Scenario: Pause duration is configurable

- **WHEN** the destruction-pause duration is changed in the configuration
- **THEN** the delay between destruction and the next round changes accordingly
