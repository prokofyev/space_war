## ADDED Requirements

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
