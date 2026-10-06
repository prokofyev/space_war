# configuration Specification

## Purpose

Defines the gameplay constants and per-player keyboard bindings as explicit,
documented configuration so movement, combat, and match behavior can be tuned
without editing core logic.

## Requirements

### Requirement: Tunable gameplay constants

Gameplay quantities SHALL be defined as named configuration values rather than
literals scattered through the logic, covering at least: ship radius, rotation
rate, thrust acceleration, missile launch speed, missile collision radius,
missile flight range or lifetime, starting and maximum ammunition, ammunition
replenish interval, and ship start positions and facings. The field dimensions
SHALL be derived from the current fullscreen display resolution rather than
hardcoded, so the playfield always spans the screen. Ship mass SHALL be equal
for both players so that collisions behave like equal-mass billiard balls.

#### Scenario: Constants are configurable in one place

- **WHEN** a gameplay constant such as thrust acceleration or missile range is
  changed in the configuration
- **THEN** the behavior that depends on it changes accordingly without editing
  unrelated logic

#### Scenario: Equal ship mass

- **WHEN** the game configures the two ships
- **THEN** both ships have the same mass so ship collisions conserve momentum
  and kinetic energy as equal-mass collisions

#### Scenario: Field dimensions follow the display

- **WHEN** the game starts in fullscreen mode
- **THEN** the configured field width and height match the current display
  resolution rather than fixed pixel dimensions

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
