import math
from dataclasses import replace

import pygame

from space_war import effects
from space_war.config import GameConfig
from space_war.render import Renderer
from space_war.world import Controls, World


def _world(config, width=200.0, height=150.0):
    # These tests care about visual effects, not gravity; isolate the bodies so
    # ships keep still while debris is checked.
    config = replace(config, gravitational_constant=0.0)
    return World(config=config, width=width, height=height)


def test_renderer_rotated_sprite_differs_across_angles():
    config = GameConfig()
    renderer = Renderer(config)
    sprite = renderer.sprites.ship[0]
    a = pygame.transform.rotozoom(sprite, 0.0, 1.0)
    b = pygame.transform.rotozoom(sprite, -90.0, 1.0)
    assert pygame.image.tostring(a, "RGBA") != pygame.image.tostring(b, "RGBA")


def test_renderer_draws_both_players_headless():
    config = GameConfig()
    surface = pygame.Surface((320, 240))
    world = _world(config, 320.0, 240.0)
    renderer = Renderer(config)
    font = pygame.font.SysFont("monospace", 14)
    renderer.update(0.016, world, [Controls(), Controls()])
    renderer.draw(surface, world, font, [Controls(), Controls()])


def test_engines_on_frame_only_while_thrusting():
    config = GameConfig()
    surface = pygame.Surface((320, 240))
    world = _world(config, 320.0, 240.0)
    renderer = Renderer(config)
    font = pygame.font.SysFont("monospace", 14)

    renderer.draw(surface, world, font, [Controls(thrust=False), Controls()])
    engines_off = surface.copy()

    renderer.draw(surface, world, font, [Controls(thrust=True), Controls()])
    engines_on = surface.copy()

    # Holding thrust swaps in the engines-on artwork, changing the frame.
    assert pygame.image.tostring(engines_on, "RGBA") != pygame.image.tostring(
        engines_off, "RGBA"
    )


def test_missile_trail_draws_without_error():
    config = GameConfig()
    surface = pygame.Surface((200, 150))
    effects.draw_missile_trail(surface, config, (100.0, 75.0), (200.0, 0.0))
    # A trail was drawn: the surface is no longer fully black.
    assert surface.get_bounding_rect().width > 0


def test_debris_spawns_spreads_and_expires():
    config = GameConfig()
    field = effects.ExplosionField(config)
    field.spawn((50.0, 50.0), (255, 0, 0))
    assert len(field.pieces) == config.debris_count
    directions = {(round(p.velocity[0], 1), round(p.velocity[1], 1)) for p in field.pieces}
    assert len(directions) > 1  # debris flies in different directions

    field.update(config.debris_lifetime + 0.1)
    assert field.pieces == []


def test_debris_is_purely_visual():
    config = GameConfig()
    world = _world(config, 200.0, 150.0)
    before = ([s.position for s in world.ships], list(world.scores), list(world.ammo))
    field = effects.ExplosionField(config)
    field.spawn((10.0, 10.0), (255, 0, 0))
    for _ in range(5):
        world.step(0.016, [Controls(), Controls()])
        field.update(0.016)
    after = ([s.position for s in world.ships], list(world.scores), list(world.ammo))
    assert before == after


def test_debris_spawns_from_destruction_event():
    config = GameConfig()
    world = _world(config, 200.0, 150.0)
    renderer = Renderer(config)
    world.ships[1].position = (60.0, 60.0)
    from space_war.entities import Missile

    world.missiles.append(
        Missile(position=(60.0, 60.0), velocity=(0.0, 0.0), owner=0)
    )
    world.step(1e-9, [Controls(), Controls()])
    renderer.update(1e-9, world, [Controls(), Controls()])
    assert renderer.explosions.pieces  # debris spawned


def test_round_reset_clears_debris():
    config = GameConfig()
    world = _world(config, 200.0, 150.0)
    renderer = Renderer(config)
    world.ships[1].position = (60.0, 60.0)
    from space_war.entities import Missile

    world.missiles.append(Missile(position=(60.0, 60.0), velocity=(0.0, 0.0), owner=0))
    world.step(1e-9, [Controls(), Controls()])
    renderer.update(1e-9, world, [Controls(), Controls()])
    assert renderer.explosions.pieces

    # Finish the pause and clear effects on the new round.
    world.step(world.config.destruction_pause + 1e-6, [Controls(), Controls()])
    renderer.update(1e-6, world, [Controls(), Controls()])
    assert renderer.explosions.pieces == []


def test_debris_inherits_ship_velocity():
    config = GameConfig()
    field = effects.ExplosionField(config)
    field.spawn((50.0, 50.0), (255, 0, 0), inherited_velocity=(120.0, 0.0))
    # Every piece carries the ship's velocity plus its own outward motion.
    assert all(p.velocity[0] > 0 for p in field.pieces)
    mean_dx = sum(p.velocity[0] for p in field.pieces) / len(field.pieces)
    assert mean_dx > 100.0


def test_debris_from_destruction_event_inherits_velocity():
    from space_war.entities import Missile

    config = GameConfig()
    world = _world(config, 200.0, 150.0)
    renderer = Renderer(config)
    victim = world.ships[1]
    victim.position = (100.0, 75.0)
    victim.velocity = (80.0, 0.0)
    world.missiles.append(Missile(position=(100.0, 75.0), velocity=(0.0, 0.0), owner=0))
    world.step(1e-9, [Controls(), Controls()])
    renderer.update(1e-9, world, [Controls(), Controls()])
    assert renderer.explosions.pieces
    mean_dx = sum(p.velocity[0] for p in renderer.explosions.pieces) / len(
        renderer.explosions.pieces
    )
    assert mean_dx > 60.0
