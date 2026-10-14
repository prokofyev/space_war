## ADDED Requirements

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

## REMOVED Requirements

### Requirement: Gravity across the borderless field

**Reason**: The borderless toroidal field no longer exists, so wrapped
shortest-path distances no longer apply.

**Migration**: Gravity now uses plain Euclidean distances between bodies on the
infinite field; "No singularity from wrapping" is subsumed by the new
no-singularity scenario.
