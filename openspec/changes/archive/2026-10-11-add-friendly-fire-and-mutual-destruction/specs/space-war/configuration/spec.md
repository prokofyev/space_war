## MODIFIED Requirements

### Requirement: Tunable gameplay constants

Gameplay quantities SHALL be defined as named configuration values rather than
literals scattered through the logic, covering at least: ship rest mass, ship
radius, rotation rate, thrust force/acceleration, missile launch speed, missile
collision radius, missile flight lifetime (in seconds), missile mass used by
gravity, starting and maximum ammunition, ammunition replenish interval, the
firing cooldown between shots, the round-end window duration, ship start
positions and facings, the speed of light `c`, and the gravitational constant
used by gravity. The field dimensions SHALL be derived from the current
fullscreen display resolution rather than hardcoded, so the playfield always
spans the screen. Ship rest mass SHALL be equal for both players so that
collisions behave like relativistic equal-mass collisions.

#### Scenario: Constants are configurable in one place

- **WHEN** a gameplay constant such as thrust, missile lifetime, the speed of
  light, the firing cooldown, or the gravitational constant is changed in the
  configuration
- **THEN** the behavior that depends on it changes accordingly without editing
  unrelated logic

#### Scenario: Equal ship mass

- **WHEN** the game configures the two ships
- **THEN** both ships have the same rest mass so ship collisions conserve
  relativistic momentum and energy as equal-mass collisions

#### Scenario: Field dimensions follow the display

- **WHEN** the game starts in fullscreen mode
- **THEN** the configured field width and height match the current display
  resolution rather than fixed pixel dimensions

#### Scenario: Speed of light is configurable

- **WHEN** the speed of light `c` is changed in the configuration
- **THEN** the highest speed any ship or missile can approach changes
  accordingly

#### Scenario: Missile lifetime is expressed in seconds

- **WHEN** the missile lifetime is changed in the configuration
- **THEN** missiles live for that many seconds of flight time before expiring

#### Scenario: Firing cooldown is configurable

- **WHEN** the firing cooldown is changed in the configuration
- **THEN** the minimum time between two shots from the same player changes
  accordingly

#### Scenario: Round-end window duration is configurable

- **WHEN** the round-end window duration is changed in the configuration
- **THEN** the delay between the first destruction in a round and the next round
  changes accordingly

#### Scenario: Gravitational constant is configurable

- **WHEN** the gravitational constant is changed in the configuration
- **THEN** the strength of gravitational attraction between bodies changes
  accordingly
