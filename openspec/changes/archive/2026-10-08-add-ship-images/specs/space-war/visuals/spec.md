## MODIFIED Requirements

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
