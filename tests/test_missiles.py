import pytest

from space_war.entities import Missile
from space_war.world import Controls, toroidal_delta


def _fire(world, player_index=0):
    return world.step(1e-9, [Controls(fire=(i == player_index)) for i in range(2)])


def test_fire_spawns_missile_and_consumes_ammo(world):
    ship = world.ships[0]
    ship.angle = 0.0
    _fire(world, 0)
    assert len(world.missiles) == 1
    assert world.ammo[0] == 2
    missile = world.missiles[0]
    assert missile.owner == 0
    assert missile.velocity[0] == world.config.missile_speed


def test_fire_combines_ship_velocity(world):
    ship = world.ships[0]
    ship.angle = 0.0
    ship.velocity = (30.0, 5.0)
    _fire(world, 0)
    missile = world.missiles[0]
    # Low-speed limit of relativistic velocity addition ~ naive sum.
    assert missile.velocity[0] == pytest.approx(
        world.config.missile_speed + 30.0, rel=1e-3
    )
    assert missile.velocity[1] == pytest.approx(5.0, rel=1e-3)


def test_empty_magazine_does_not_fire(world):
    world.ammo[0] = 0
    _fire(world, 0)
    assert world.missiles == []


def test_replenishment_adds_one_per_interval(world):
    world.ammo[0] = 1
    world.recharge[0] = 0.0
    # Advance below one interval: no new missile yet.
    world.step(world.config.ammo_replenish_interval * 0.5, [Controls(), Controls()])
    assert world.ammo[0] == 1
    world.step(world.config.ammo_replenish_interval * 0.5 + 1e-6, [Controls(), Controls()])
    assert world.ammo[0] == 2


def test_replenishment_never_exceeds_capacity(world):
    world.ammo[0] = world.config.ammo_max
    world.step(world.config.ammo_replenish_interval * 5, [Controls(), Controls()])
    assert world.ammo[0] == world.config.ammo_max


def test_replenishment_resets_on_round_start(world):
    world.ammo = [0, 2]
    world.reset_round()
    assert world.ammo == [world.config.ammo_start, world.config.ammo_start]
    assert world.recharge == [0.0, 0.0]


def test_missile_expires_by_range_without_scoring(world):
    world.missiles.append(
        Missile(
            position=(50.0, 50.0),
            velocity=(world.config.missile_speed, 0.0),
            owner=0,
            traveled=world.config.missile_range - 1.0,
        )
    )
    world.step(0.1, [Controls(), Controls()])
    assert world.missiles == []
    assert world.scores == [0, 0]


def test_missile_wraps_edges(world):
    world.missiles.append(
        Missile(position=(99.0, 50.0), velocity=(50.0, 0.0), owner=0, traveled=0.0)
    )
    world.step(0.1, [Controls(), Controls()])
    missile = world.missiles[0]
    assert missile.position[0] < 50.0


def test_missile_hit_destroys_enemy_and_scores(world):
    enemy = world.ships[1]
    enemy.position = (50.0, 50.0)
    world.missiles.append(
        Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=0, traveled=0.0)
    )
    world.step(1e-9, [Controls(), Controls()])
    assert world.scores == [1, 0]
    # The destruction pause started; the ship is not respawned yet.
    assert not world.ships[1].alive
    assert world.missiles == []
    # After the pause the new round restarts both ships.
    world.step(world.config.destruction_pause + 1e-6, [Controls(), Controls()])
    assert world.ships[1].alive


def test_missile_does_not_hit_own_ship(world):
    own = world.ships[0]
    own.position = (50.0, 50.0)
    world.missiles.append(
        Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=0, traveled=0.0)
    )
    world.step(1e-9, [Controls(), Controls()])
    assert own.alive
    assert world.scores == [0, 0]


def test_missile_interception_removes_both(world):
    world.missiles.append(Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=0))
    world.missiles.append(Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=1))
    world.step(1e-9, [Controls(), Controls()])
    assert world.missiles == []
    assert world.scores == [0, 0]
    assert all(ship.alive for ship in world.ships)
