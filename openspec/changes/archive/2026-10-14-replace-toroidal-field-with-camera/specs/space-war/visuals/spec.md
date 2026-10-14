## ADDED Requirements

### Requirement: Camera keeps both ships framed

The render layer SHALL draw the infinite world through a camera that places the
midpoint between the two ships at the center of the display and chooses a single
uniform scale for both axes so that both ships always fit within the display
with a configured margin. When the ships are farther apart than the native 1:1
view can show, the camera SHALL zoom out until they fit; when they are closer,
the camera SHALL zoom in and may magnify the ships beyond their native size.
There SHALL be no maximum zoom cap. The zoom and the tracked midpoint SHALL
change smoothly over time rather than jumping between frames. Missiles and other
objects SHALL be drawn with the same camera transform but are not required to
remain on screen.

#### Scenario: Both ships stay visible as they separate

- **WHEN** the two ships move apart
- **THEN** the camera zooms out smoothly so that both ships remain fully within
  the display with the configured margin

#### Scenario: Camera zooms in when ships are close

- **WHEN** the two ships are close together
- **THEN** the camera zooms in so they fill more of the display, magnifying them
  beyond their native size

#### Scenario: One uniform scale for both axes

- **WHEN** the camera draws the world
- **THEN** the horizontal and vertical scales are equal, so the world is not
  distorted

#### Scenario: Initial zoom frames the configured start distance

- **WHEN** a round starts with the ships at `initial_ship_distance` apart
- **THEN** the camera's initial scale frames both ships within the display
  without an abrupt jump on the first frame

#### Scenario: Camera motion is smooth

- **WHEN** the ships' separation or midpoint changes between frames
- **THEN** the camera's scale and center move toward the new target gradually
  instead of snapping instantly
