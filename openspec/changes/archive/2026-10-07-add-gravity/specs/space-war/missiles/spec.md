## MODIFIED Requirements

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
