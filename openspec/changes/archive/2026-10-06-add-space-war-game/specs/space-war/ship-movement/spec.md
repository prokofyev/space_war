## Purpose

Defines how the two player ships move on the playfield: rotation, inertia,
thrust-or-brake acceleration relative to the current velocity, seamless
wrapping at the field edges, and damage-free elastic collisions between ships.

## ADDED Requirements

### Requirement: Ship rotation control

Each ship SHALL have its own independent facing angle and SHALL rotate
clockwise or counter-clockwise only while the corresponding rotation key is
held. Rotation SHALL NOT change the ship's velocity.

#### Scenario: Rotate clockwise

- **WHEN** a player holds the clockwise rotation key
- **THEN** that player's ship facing angle increases continuously at the
  configured rotation rate
- **AND** the ship's velocity vector is unchanged

#### Scenario: Rotate counter-clockwise

- **WHEN** a player holds the counter-clockwise rotation key
- **THEN** that player's ship facing angle decreases continuously at the
  configured rotation rate
- **AND** the ship's velocity vector is unchanged

#### Scenario: No rotation key held

- **WHEN** neither rotation key for a player is held
- **THEN** that ship's facing angle stays constant

### Requirement: Thrust and inertia

Thrust SHALL be applied only while a player's thrust key is held, and SHALL
accelerate the ship along its facing direction. The ship SHALL move under
inertia when thrust is not applied, preserving its velocity (no automatic
drag). Rotating while thrusting SHALL let the player steer the ship.

#### Scenario: Coasting without thrust

- **WHEN** a ship is moving and its thrust key is not held
- **THEN** the ship continues at its current velocity and position advances by
  velocity multiplied by elapsed time

#### Scenario: Accelerating along facing direction

- **WHEN** a player holds thrust while the ship faces along or near its
  velocity direction
- **THEN** the ship's speed increases in the direction it is facing

### Requirement: Thrust relative to velocity (accelerate or brake)

The thrust SHALL add a fixed acceleration vector along the ship's facing
direction to the current velocity. Because the contribution of thrust depends
on the angle between the velocity vector and the facing direction, thrusting
can either speed the ship up, slow it down, or deflect its course without
changing its path shape beyond that contribution.

#### Scenario: Thrust opposite to velocity brakes the ship

- **WHEN** a ship moving at a positive speed points its facing roughly
  opposite to its velocity and holds thrust
- **THEN** the ship's speed decreases

#### Scenario: Thrust aligned with velocity accelerates the ship

- **WHEN** a ship points its facing roughly along its velocity and holds thrust
- **THEN** the ship's speed increases

#### Scenario: Thrust perpendicular to velocity deflects the ship

- **WHEN** a ship points its facing perpendicular to its velocity and holds
  thrust
- **THEN** the ship's velocity direction changes toward the facing direction
  while its speed changes according to the angle between velocity and thrust

### Requirement: Borderless toroidal playfield

The playfield SHALL have no walls. Any ship that leaves one edge SHALL
re-enter from the opposite edge while preserving its position offset, velocity,
and facing angle relative to the field.

#### Scenario: Exit through the top edge

- **WHEN** a ship's position moves above the top edge of the field
- **THEN** the ship re-enters at the bottom edge at the same horizontal
  position and keeps its velocity and facing angle

#### Scenario: Exit through the right edge

- **WHEN** a ship's position moves beyond the right edge of the field
- **THEN** the ship re-enters at the left edge at the same vertical position
  and keeps its velocity and facing angle

#### Scenario: Diagonal exit wraps both axes

- **WHEN** a ship crosses a corner so that it leaves both a vertical and a
  horizontal edge
- **THEN** the ship re-enters at the diagonally opposite corner with velocity
  and facing angle unchanged

### Requirement: Damage-free elastic ship collision

When two ships overlap, they SHALL resolve the collision as an elastic
collision of two rigid bodies of equal mass, conserving total momentum and
total kinetic energy. The collision SHALL NOT change either player's score or
destroy a ship.

#### Scenario: Head-on collision reverses relative motion

- **WHEN** two equal-mass ships collide head-on along the line connecting their
  centers
- **THEN** each ship's velocity component along that line is exchanged with
  the other ship's, so their relative motion reverses
- **AND** no ship is destroyed and no score changes

#### Scenario: Glancing collision conserves momentum and energy

- **WHEN** two equal-mass ships collide while not aligned through their centers
- **THEN** the total momentum of the two ships is the same before and after the
  collision
- **AND** the total kinetic energy of the two ships is the same before and
  after the collision
- **AND** the ships are separated so they no longer overlap immediately after
  the collision
