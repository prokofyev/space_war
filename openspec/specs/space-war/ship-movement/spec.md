# ship-movement Specification

## Purpose

Defines how the two player ships move on the playfield: rotation, inertia,
thrust-or-brake acceleration relative to the current velocity, unbounded
movement on an infinite plane, and damage-free relativistic elastic collisions
between ships.

## Requirements

### Requirement: Relativistic mass and speed of light

Motion SHALL follow special relativity: each ship SHALL have a rest mass, and its
inertia SHALL grow with speed as `gamma * m0`, where `gamma = 1 /
sqrt(1 - (v / c)^2)`. The speed of light `c` SHALL be a configurable upper
bound, and no ship SHALL ever reach or exceed it.

#### Scenario: Relativistic mass grows with speed

- **WHEN** a ship's speed increases toward `c`
- **THEN** its relativistic mass increases, so the same force produces a
  smaller acceleration than at low speed

#### Scenario: Speed of light is unreachable

- **WHEN** thrust is applied for an arbitrarily long time
- **THEN** the ship's speed approaches `c` asymptotically and always remains
  strictly below `c`

#### Scenario: Speed of light is configurable

- **WHEN** `c` is changed in the configuration
- **THEN** the highest speed a ship can approach changes accordingly without
  editing movement logic

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
change the ship's momentum along its facing direction (as a force acting over
time), with velocity derived from momentum via the relativistic relation.
Because relativistic mass grows with speed, the resulting acceleration
diminishes as the ship approaches `c`, so speed only approaches the limit.
Between thrust inputs the ship SHALL move under inertia, but it is also
subject to gravity from other bodies, so its velocity is not necessarily
constant and its path is not necessarily straight. Rotating while thrusting
SHALL let the player steer the ship.

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

### Requirement: Thrust relative to velocity (accelerate or brake)

Thrust SHALL change the ship's momentum along its facing direction. Because the
contribution of thrust depends on the angle between the velocity vector and the
facing direction, thrusting can either speed the ship up, slow it down, or
deflect its course. Relativistic mass growth SHALL reduce acceleration near `c`
but SHALL NOT prevent slowing down or turning.

#### Scenario: Thrust opposite to velocity brakes the ship

- **WHEN** a ship moving at a positive speed points its facing roughly
  opposite to its velocity and holds thrust
- **THEN** the ship's speed decreases

#### Scenario: Thrust aligned with velocity accelerates the ship

- **WHEN** a ship points its facing roughly along its velocity and holds thrust
  below the speed of light
- **THEN** the ship's speed increases

#### Scenario: Thrust perpendicular to velocity deflects the ship

- **WHEN** a ship points its facing perpendicular to its velocity and holds
  thrust
- **THEN** the ship's velocity direction changes toward the facing direction
  while its speed changes according to the angle between velocity and thrust

#### Scenario: Acceleration diminishes near the speed of light

- **WHEN** a ship near `c` thrusts along its velocity
- **THEN** the resulting speed stays strictly below `c` and the gain per unit of
  thrust is smaller than at low speed

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

### Requirement: Damage-free elastic ship collision

When two ships overlap, they SHALL resolve the collision as a relativistic
elastic collision of two equal rest-mass bodies, conserving total relativistic
momentum and total relativistic energy, so that neither ship's speed reaches or
exceeds `c`. The collision SHALL NOT change either player's score or destroy a
ship. When both ships are slow compared to `c`, the result SHALL approach the
Newtonian equal-mass elastic collision.

#### Scenario: Head-on collision reverses relative motion

- **WHEN** two equal rest-mass ships collide head-on along the line connecting
  their centers at speeds well below `c`
- **THEN** each ship's velocity component along that line is exchanged with
  the other ship's, so their relative motion reverses
- **AND** no ship is destroyed and no score changes

#### Scenario: Glancing collision conserves momentum and energy

- **WHEN** two equal rest-mass ships collide while not aligned through their
  centers
- **THEN** the total relativistic momentum of the two ships is conserved before
  and after the collision
- **AND** the total relativistic energy of the two ships is conserved before
  and after the collision
- **AND** neither ship's speed reaches or exceeds `c`
- **AND** the ships are separated so they no longer overlap immediately after
  the collision

#### Scenario: Fast collision cannot exceed the speed of light

- **WHEN** two ships collide at speeds close to `c`
- **THEN** the resulting speeds remain strictly below `c`
