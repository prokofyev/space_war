## ADDED Requirements

### Requirement: Infinite playfield without wrapping

The playfield SHALL be an infinite plane with no walls and no edges. A ship
SHALL move freely under its velocity and thrust, and SHALL NOT be teleported,
wrapped, or otherwise repositioned when it moves away from the origin. Its
position SHALL be allowed to grow or shrink without bound.

#### Scenario: A ship is never teleported by an edge

- **WHEN** a ship moves in a straight line for an extended time
- **THEN** its position changes continuously by velocity multiplied by elapsed
  time, with no wrap or jump to another part of the field

#### Scenario: Ships may fly apart without limit

- **WHEN** two ships move apart
- **THEN** the distance between them grows without bound and neither ship is
  stopped or redirected by the absence of a boundary

## REMOVED Requirements

### Requirement: Borderless toroidal playfield

**Reason**: The finite toroidal field is replaced by an infinite plane; the
seam teleported ships and made it impossible to keep both ships framed.

**Migration**: Ships now move on an unbounded plane and are never wrapped. The
camera, not the field, keeps both ships on screen.
