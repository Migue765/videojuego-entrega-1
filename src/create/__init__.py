import math
import random

import esper

from src.ecs.components import (
    CTransform, CVelocity, CShape, CEnemySpawner, SpawnEvent,
    CTagPlayer, CTagBullet, CTagEnemy, CInputCommand
)


def create_rectangle(world: esper.World, x: float, y: float,
                     w: int, h: int, color: tuple,
                     speed_min: float, speed_max: float) -> int:
    """Creates an enemy rectangle with a random velocity and the CTagEnemy tag."""
    speed = random.uniform(speed_min, speed_max)
    angle = random.uniform(0, 2 * math.pi)
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)

    entity = world.create_entity()
    world.add_component(entity, CTransform(x=x, y=y))
    world.add_component(entity, CVelocity(vx=vx, vy=vy))
    world.add_component(entity, CShape(w=w, h=h, r=color[0], g=color[1], b=color[2]))
    world.add_component(entity, CTagEnemy())
    return entity


def create_enemy_spawner(world: esper.World, level_data: dict, enemies_data: dict) -> int:
    events = []
    for ev in level_data.get("enemy_spawn_events", []):
        events.append(SpawnEvent(
            time=ev["time"],
            enemy_type=ev["enemy_type"],
            x=ev["position"]["x"],
            y=ev["position"]["y"]
        ))

    spawner = CEnemySpawner(events=events, enemies_data=enemies_data)
    entity = world.create_entity()
    world.add_component(entity, spawner)
    return entity


def create_player(world: esper.World, x: float, y: float,
                  w: int, h: int, color: tuple) -> int:
    """Creates the player rectangle. No CVelocity — movement is handled via CInputCommand."""
    entity = world.create_entity()
    world.add_component(entity, CTransform(x=x, y=y))
    world.add_component(entity, CShape(w=w, h=h, r=color[0], g=color[1], b=color[2]))
    world.add_component(entity, CTagPlayer())
    world.add_component(entity, CInputCommand())
    return entity


def create_bullet(world: esper.World, origin_x: float, origin_y: float,
                  target_x: float, target_y: float,
                  w: int, h: int, color: tuple, speed: float):
    """Creates a bullet fired from the player center toward the mouse position."""
    dx = target_x - origin_x
    dy = target_y - origin_y
    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0:
        return None

    vx = (dx / dist) * speed
    vy = (dy / dist) * speed

    entity = world.create_entity()
    world.add_component(entity, CTransform(x=origin_x - w / 2, y=origin_y - h / 2))
    world.add_component(entity, CVelocity(vx=vx, vy=vy))
    world.add_component(entity, CShape(w=w, h=h, r=color[0], g=color[1], b=color[2]))
    world.add_component(entity, CTagBullet())
    return entity
