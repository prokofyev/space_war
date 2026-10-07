## MODIFIED Requirements

### Requirement: Thrust and inertia

Thrust SHALL be applied only while a player's thrust key is held, and SHALL
change the ship's momentum along its facing direction (as a force acting over
time), with velocity derived from momentum via the relativistic relation.
Because relativistic mass grows with speed, the resulting acceleration
diminishes as the ship approaches `c`, so speed only approaches the limit.
Between thrust inputs the ship SHALL move under inertia, but it is also subject
to gravity from other bodies, so its velocity is not necessarily constant and
its path is not necessarily straight. Rotating while thrusting SHALL let the
player steer the ship.

#### Scenario: Coasting without thrust

- **WHEN** a ship is moving with no thrust and no other body close enough for
  gravity to matter
- **THEN** the ship continues at approximately its current velocity and its
  position advances by velocity multiplied by elapsed time

#### Scenario: Other bodies bend a coasting ship's path

- **WHEN** a ship coasts under the gravitational attraction of another body
- **THEN** its velocity changes toward that body and its path curves instead of
  remaining a straight line

#### Scenario: Accelerating along facing direction

- **WHEN** a player holds thrust while the ship faces along or near its
  velocity direction and its speed is well below `c`
- **THEN** the ship's speed increases in the direction it is facing, closely
  matching the low-speed (Newtonian) acceleration
