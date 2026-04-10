import esper

from src.ecs.components import CTransform, CShape, CInputCommand, CTagPlayer, CTagBullet
from src.ecs.commands import PlayerAction
from src.create import create_bullet


def system_player_movement(world: esper.World, delta_time: float, speed: float):
    """Moves the player rectangle based on active input commands."""
    for _, (_, transform, cmd) in world.get_components(CTagPlayer, CTransform, CInputCommand):
        if PlayerAction.PLAYER_LEFT in cmd.actions:
            transform.x -= speed * delta_time
        if PlayerAction.PLAYER_RIGHT in cmd.actions:
            transform.x += speed * delta_time
        if PlayerAction.PLAYER_UP in cmd.actions:
            transform.y -= speed * delta_time
        if PlayerAction.PLAYER_DOWN in cmd.actions:
            transform.y += speed * delta_time


def system_player_boundary(world: esper.World, window_w: int, window_h: int):
    """Prevents the player from leaving the screen."""
    for _, (_, transform, shape) in world.get_components(CTagPlayer, CTransform, CShape):
        transform.x = max(0.0, min(transform.x, window_w - shape.w))
        transform.y = max(0.0, min(transform.y, window_h - shape.h))


def system_player_fire(world: esper.World, bullet_cfg: dict, max_bullets: int):
    """Creates a bullet toward the mouse when the fire action is active."""
    bullet_count = sum(1 for _ in world.get_component(CTagBullet))
    if bullet_count >= max_bullets:
        return

    for _, (_, transform, shape, cmd) in world.get_components(
            CTagPlayer, CTransform, CShape, CInputCommand):
        if PlayerAction.PLAYER_FIRE in cmd.actions:
            center_x = transform.x + shape.w / 2
            center_y = transform.y + shape.h / 2
            create_bullet(
                world,
                origin_x=center_x,
                origin_y=center_y,
                target_x=cmd.mouse_x,
                target_y=cmd.mouse_y,
                w=bullet_cfg["size"]["w"],
                h=bullet_cfg["size"]["h"],
                color=(
                    bullet_cfg["color"]["r"],
                    bullet_cfg["color"]["g"],
                    bullet_cfg["color"]["b"]
                ),
                speed=bullet_cfg["speed"]
            )
