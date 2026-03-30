import pygame
import esper

from src.ecs.components import CTransform, CVelocity, CShape, CEnemySpawner
from src.create import create_rectangle


def system_movement(world: esper.World, delta_time: float):
    for _, (transform, velocity) in world.get_components(CTransform, CVelocity):
        transform.x += velocity.vx * delta_time
        transform.y += velocity.vy * delta_time


def system_bounce(world: esper.World, window_w: int, window_h: int):
    for _, (transform, velocity, shape) in world.get_components(CTransform, CVelocity, CShape):
        if transform.x < 0:
            transform.x = 0
            velocity.vx = abs(velocity.vx)
        elif transform.x + shape.w > window_w:
            transform.x = window_w - shape.w
            velocity.vx = -abs(velocity.vx)

        if transform.y < 0:
            transform.y = 0
            velocity.vy = abs(velocity.vy)
        elif transform.y + shape.h > window_h:
            transform.y = window_h - shape.h
            velocity.vy = -abs(velocity.vy)


def system_render(world: esper.World, surface: pygame.Surface):
    for _, (transform, shape) in world.get_components(CTransform, CShape):
        pygame.draw.rect(
            surface,
            (shape.r, shape.g, shape.b),
            pygame.Rect(int(transform.x), int(transform.y), shape.w, shape.h)
        )


def system_enemy_spawner(world: esper.World, delta_time: float):
    for _, spawner in world.get_component(CEnemySpawner):
        spawner.elapsed += delta_time
        for event in spawner.events:
            if not event.triggered and spawner.elapsed >= event.time:
                enemy_data = spawner.enemies_data.get(event.enemy_type)
                if enemy_data:
                    create_rectangle(
                        world,
                        x=event.x,
                        y=event.y,
                        w=enemy_data["size"]["x"],
                        h=enemy_data["size"]["y"],
                        color=(
                            enemy_data["color"]["r"],
                            enemy_data["color"]["g"],
                            enemy_data["color"]["b"]
                        ),
                        speed_min=enemy_data["velocity_min"],
                        speed_max=enemy_data["velocity_max"]
                    )
                event.triggered = True
