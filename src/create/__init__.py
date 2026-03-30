import math
import random

import esper

from src.ecs.components import CTransform, CVelocity, CShape, CEnemySpawner, SpawnEvent


def create_rectangle(world: esper.World, x: float, y: float,
                     w: int, h: int, color: tuple,
                     speed_min: float, speed_max: float) -> int:
    speed = random.uniform(speed_min, speed_max)
    angle = random.uniform(0, 2 * math.pi)
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)

    entity = world.create_entity()
    world.add_component(entity, CTransform(x=x, y=y))
    world.add_component(entity, CVelocity(vx=vx, vy=vy))
    world.add_component(entity, CShape(w=w, h=h, r=color[0], g=color[1], b=color[2]))
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
