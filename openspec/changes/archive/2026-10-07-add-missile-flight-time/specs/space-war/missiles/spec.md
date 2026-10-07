## MODIFIED Requirements

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
