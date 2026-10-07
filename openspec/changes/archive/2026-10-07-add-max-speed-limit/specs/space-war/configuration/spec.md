## MODIFIED Requirements

### Requirement: Tunable gameplay constants

Gameplay quantities SHALL be defined as named configuration values rather than
literals scattered through the logic, covering at least: ship rest mass, ship
radius, rotation rate, thrust force/acceleration, missile launch speed, missile
collision radius, missile flight range or lifetime, starting and maximum
ammunition, ammunition replenish interval, ship start positions and facings, and
the speed of light `c` used by the relativistic model. The field dimensions
SHALL be derived from the current fullscreen display resolution rather than
hardcoded, so the playfield always spans the screen. Ship rest mass SHALL be
equal for both players so that collisions behave like relativistic equal-mass
collisions.

#### Scenario: Constants are configurable in one place

- **WHEN** a gameplay constant such as thrust, missile range, or the speed of
  light is changed in the configuration
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
