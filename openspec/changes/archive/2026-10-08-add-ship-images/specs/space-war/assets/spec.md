## Purpose

Bundles the authored ship artwork as image files shipped inside the package and
defines which file is used for each player and for the idle versus thrusting
state, so ship rendering is driven by data rather than by one-off code.

## ADDED Requirements

### Requirement: Bundled ship artwork

The game SHALL ship the authored ship images as files stored inside the
`space_war` package (not in the project root), so the assets travel with the
code and are found regardless of the working directory the game is launched
from.

#### Scenario: Artwork lives inside the package

- **WHEN** the ship images are inspected in the repository
- **THEN** they reside in a dedicated assets directory inside the `space_war`
  package rather than in the project root

#### Scenario: Artwork loads at runtime

- **WHEN** the game builds its ship sprites
- **THEN** it loads the ship images from their bundled location without relying
  on the current working directory

### Requirement: Artwork is mapped to players and engine states

The game SHALL provide, for each of the two players, two ship images: an
"engines off" image and an "engines on" image. Player one SHALL use the blue
ship artwork and player two SHALL use the red ship artwork, so the two ships
stay visually distinct.

#### Scenario: Player colours come from the artwork

- **WHEN** both ships are drawn
- **THEN** player one is rendered from the blue ship image and player two from
  the red ship image, keeping the two ships distinguishable

#### Scenario: Each player has an idle and a thrusting image

- **WHEN** the game builds its ship sprites
- **THEN** each player has both an engines-off image and an engines-on image
  available for rendering

### Requirement: Image background is removed

The ship images SHALL be drawn with their background removed, so a ship appears
as a cut-out of its silhouette rather than as an opaque rectangle, and the
background shows through everywhere the image is not part of the ship.

#### Scenario: Ship is drawn as a cut-out

- **WHEN** a ship is drawn over the playfield
- **THEN** the area of the image that is not the ship does not cover the
  playfield, so only the ship shape is visible
