from space_war.entities import Missile
from space_war.world import Controls


def test_no_double_scoring_in_single_step(world):
    # The enemy ship is hit by two missiles in the same step. The round must
    # resolve once: exactly one point is awarded, not two.
    world.ships[0].position = (10.0, 10.0)
    world.ships[1].position = (50.0, 50.0)
    world.missiles.append(Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=0))
    world.missiles.append(Missile(position=(50.0, 50.0), velocity=(0.0, 0.0), owner=0))
    world.step(1e-9, [Controls(), Controls()])
    assert sum(world.scores) == 1


def test_expired_missile_does_not_hit(world):
    # A missile that reaches its range in this step must be removed before the
    # hit check, so it cannot kill a ship it happens to overlap.
    enemy = world.ships[1]
    enemy.position = (50.0, 50.0)
    world.missiles.append(
        Missile(
            position=(50.0, 50.0),
            velocity=(0.0, 0.0),
            owner=0,
            traveled=world.config.missile_range,  # already expired
        )
    )
    world.step(1e-9, [Controls(), Controls()])
    assert enemy.alive
    assert world.scores == [0, 0]
