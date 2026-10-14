# configuration Specification

## Purpose

Defines the gameplay constants and per-player keyboard bindings as explicit,
documented configuration so movement, combat, and match behavior can be tuned
without editing core logic.

## Requirements

### Requirement: Tunable gameplay constants

Gameplay quantities SHALL be defined as named configuration values rather than
literals scattered through the logic, covering at least: ship rest mass, ship
radius, rotation rate, thrust force/acceleration, missile launch speed, missile
collision radius, missile flight lifetime (in seconds), missile mass used by
gravity, starting and maximum ammunition, ammunition replenish interval, the
firing cooldown between shots, the round-end window duration, the initial
distance between the two ships and their facings, the camera framing margin and
smoothing rate, the speed of light `c`, and the gravitational constant used by
gravity. The world SHALL be infinite, so no field width or height SHALL be
derived from the display resolution or hardcoded. Ship rest mass SHALL be equal
for both players so that collisions behave like relativistic equal-mass
collisions.

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
- **THEN** the camera derives its initial zoom from the configured initial ship
  distance and the current display resolution so both ships are framed on
  screen, while the world itself is unbounded and independent of the resolution

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

### Requirement: Initial ship placement

The configuration SHALL define the starting distance between the two ships as
`initial_ship_distance` in world units, replacing display-fraction start
positions. The two ships SHALL start centered on the origin, separated by that
distance along the horizontal axis and facing each other.

#### Scenario: Ships start at the configured distance

- **WHEN** a new match or round begins
- **THEN** the two ships are placed symmetrically about the origin, separated
  by `initial_ship_distance`, facing each other

#### Scenario: Changing the start distance moves both ships

- **WHEN** `initial_ship_distance` is changed in the configuration
- **THEN** the initial separation between the two ships changes accordingly
  without editing unrelated logic

### Requirement: Per-player key bindings

The configuration SHALL define distinct, non-overlapping keyboard bindings for
each player for rotate counter-clockwise, rotate clockwise, thrust, and fire.
The controls SHALL be documented so both players know which keys to use.

#### Scenario: Distinct bindings per player

- **WHEN** a player uses their movement, rotation, and fire keys
- **THEN** those keys map only to that player and do not also control the other
  player

#### Scenario: Controls are documented

- **WHEN** a user reads the project documentation
- **THEN** it lists each player's rotation, thrust, and fire keys
