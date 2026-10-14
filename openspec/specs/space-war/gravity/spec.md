# gravity Specification

## Purpose

Defines the universal gravitational attraction between all bodies on the
playfield: every ship and missile attracts every other, the force obeys an
inverse-square law, and it is applied through the relativistic momentum model on
an infinite plane.

## Requirements

### Requirement: Mutual gravitational attraction

Every body on the playfield SHALL attract every other body: ships and missiles
alike are both gravitational sources and gravitational targets. The attraction
between two bodies SHALL be directed along the line joining them and SHALL pull
them toward each other.

#### Scenario: Two bodies attract each other

- **WHEN** two bodies are placed on the field with no other forces acting
- **THEN** each body accelerates toward the other along the line joining them

#### Scenario: Missiles are affected and attract

- **WHEN** a missile is in flight near a ship
- **THEN** the missile is pulled toward the ship, and the ship is pulled toward
  the missile

#### Scenario: Every pair participates

- **WHEN** several bodies are present
- **THEN** the net gravitational force on each body is the sum of its pairwise
  attractions to all other bodies

### Requirement: Inverse-square force law

The gravitational force between two bodies SHALL be proportional to the product
of their masses and inversely proportional to the square of the distance between
them, scaled by a configurable gravitational constant.

#### Scenario: Heavier bodies attract more strongly

- **WHEN** the mass of one body is increased while the distance is unchanged
- **THEN** the gravitational force between the two bodies increases
  proportionally

#### Scenario: Force falls off with distance

- **WHEN** the distance between two bodies is doubled
- **THEN** the gravitational force between them drops to about a quarter

#### Scenario: Gravitational constant is configurable

- **WHEN** the gravitational constant is changed in the configuration
- **THEN** the strength of all gravitational attraction changes accordingly
  without editing the force logic

### Requirement: Gravity on an infinite field

Gravitational distances SHALL be measured as the ordinary straight-line
(Euclidean) distance between bodies on the infinite field. There SHALL be no
wrapping and no shortest-path edge behavior, because the field has no edges.

#### Scenario: Distance is the straight line between bodies

- **WHEN** two bodies are far apart on the field
- **THEN** the gravitational force uses their plain separation distance and
  direction, not a wrapped alternative

#### Scenario: No singularity for coincident bodies

- **WHEN** two bodies are at the same position or very close
- **THEN** the gravitational calculation remains finite and does not produce NaN
  or infinite acceleration

### Requirement: Gravity changes momentum relativistically

Gravitational force SHALL be applied over time by changing each body's momentum,
consistent with the existing relativistic force model, so gravity never pushes a
body to or beyond the speed of light.

#### Scenario: Gravity accelerates through momentum

- **WHEN** gravity acts on a body over a time step
- **THEN** the body's momentum changes by the gravitational force times the time
  step, and its velocity is derived from the new momentum

#### Scenario: Gravity cannot exceed the speed of light

- **WHEN** gravity acts on a body already moving at a large fraction of the
  speed of light
- **THEN** the body's speed stays strictly below the speed of light
