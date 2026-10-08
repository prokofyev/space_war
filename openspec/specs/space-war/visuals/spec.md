# visuals Specification

## Purpose

Defines the procedural look of ships and missiles and the visual feedback for
ship destruction: a ship silhouette whose orientation is readable, depth and a
glow halo, a thrust flame, missile trails, and an explosion with debris. All of
this is presentational only and never changes simulation behavior.

## Requirements

### Requirement: Readable ship orientation

Each ship SHALL be drawn from its bundled ship image and oriented so that the
image's facing direction corresponds to the ship's angle used by the
simulation, so that a viewer can tell which way a ship points and can see it
rotate as it turns. The drawn silhouette SHALL make the facing direction
readable.

#### Scenario: Facing direction is visible

- **WHEN** a ship is drawn at any angle
- **THEN** the image is rotated so its nose points along the ship's simulation
  angle, making the facing direction apparent

#### Scenario: Rotation is visible over time

- **WHEN** a ship rotates
- **THEN** the drawn image rotates with it so the change in facing is apparent
  between frames

### Requirement: Ship depth and glow

Each ship SHALL be drawn from its authored image, which provides the presentational
depth and colouring, and SHALL retain a soft glow halo around it. The ship's
player colour SHALL remain visually distinct through the artwork (blue versus
red). Smooth (anti-aliased) edges SHALL be used so the ship does not look like a
hard-edged primitive.

#### Scenario: Ship is shaded and glowing

- **WHEN** a ship is drawn
- **THEN** it is rendered from an image that shows depth rather than a single
  flat colour
- **AND** a soft glow surrounds it

#### Scenario: Players remain distinguishable

- **WHEN** both ships are drawn
- **THEN** each is rendered from its own player's artwork so the two ships stay
  visually distinct

### Requirement: Thrust flame

While a player holds the thrust key, that ship SHALL be drawn using its
"engines on" image, which shows a lit engine exhaust. When thrust is not held,
the ship SHALL be drawn using its "engines off" image, showing no exhaust.

#### Scenario: Flame while thrusting

- **WHEN** a player holds the thrust key
- **THEN** the ship is drawn with its engines-on image showing a lit exhaust

#### Scenario: No flame when coasting

- **WHEN** a player is not holding the thrust key
- **THEN** the ship is drawn with its engines-off image showing no exhaust

### Requirement: Missile trail

Each missile SHALL be drawn with a light trail behind it that fades with
distance, oriented opposite the missile's velocity, so moving missiles are easy
to follow. The trail SHALL NOT affect collision detection.

#### Scenario: Missile leaves a fading trail

- **WHEN** a missile is in flight
- **THEN** a fading trail is drawn behind it along the reverse of its velocity

#### Scenario: Trail does not change gameplay

- **WHEN** missiles are drawn with trails
- **THEN** missile and ship hit detection, ammunition, and scoring are
  unchanged

### Requirement: Ship explosion with debris

When a missile destroys a ship, the display SHALL show an explosion at the
destroyed ship's position, consisting of a burst plus multiple debris pieces
that fly outward, slow down, and fade out over a short lifetime. Different
debris pieces SHALL take different outward directions so they spread out. The
debris cloud SHALL also inherit the destroyed ship's velocity, so it drifts
with the ship's momentum, and the whole cloud SHALL move continuously while
other objects keep advancing during the destruction pause.

#### Scenario: Explosion appears on destruction

- **WHEN** a missile destroys a ship
- **THEN** an explosion is drawn at that ship's position and debris pieces fly
  outward from it

#### Scenario: Debris inherits the ship's velocity

- **WHEN** a ship was moving when it was destroyed
- **THEN** its debris pieces carry the ship's velocity in addition to their own
  outward motion, so the whole cloud drifts in the direction the ship was
  heading

#### Scenario: Debris spread and fade

- **WHEN** the explosion is playing
- **THEN** its debris pieces move in different directions, decelerate, and fade
  out, disappearing within the debris lifetime

#### Scenario: Debris is purely visual

- **WHEN** debris is present
- **THEN** it does not collide with ships or missiles, does not deal damage, and
  does not change movement, ammunition, or scoring

### Requirement: Explosion visibility before respawn

The destruction pause that delays a round restart SHALL be long enough for the
explosion to be visible, and the explosion SHALL be cleared when a new round
begins so debris from one round does not carry into the next.

#### Scenario: Explosion is visible before the new round

- **WHEN** a ship is destroyed
- **THEN** the explosion plays during the destruction pause before the ships
  respawn

#### Scenario: Debris cleared on new round

- **WHEN** a new round begins
- **THEN** no debris or explosion from the previous round remains
