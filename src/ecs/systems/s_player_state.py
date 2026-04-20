import esper

from src.ecs.components import (
    CTransform, CSurface, CAnimation, CInputCommand, CTagPlayer, CTagBullet,
)
from src.ecs.commands import PlayerAction
from src.create import create_bullet


def system_player_movement(world: esper.World, delta_time: float, speed: float):
    """Moves the player sprite based on active input commands."""
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
    """Keeps the player inside the screen, using the sprite area."""
    for _, (_, transform, sprite) in world.get_components(CTagPlayer, CTransform, CSurface):
        transform.x = max(0.0, min(transform.x, window_w - sprite.area.width))
        transform.y = max(0.0, min(transform.y, window_h - sprite.area.height))


def system_player_animation_state(world: esper.World):
    """Switches the player animation between IDLE and MOVE based on input actions."""
    move_actions = (
        PlayerAction.PLAYER_LEFT,
        PlayerAction.PLAYER_RIGHT,
        PlayerAction.PLAYER_UP,
        PlayerAction.PLAYER_DOWN,
    )
    for _, (_, cmd, anim) in world.get_components(CTagPlayer, CInputCommand, CAnimation):
        moving = any(a in cmd.actions for a in move_actions)
        anim.play("MOVE" if moving else "IDLE")


def system_player_fire(world: esper.World, bullet_cfg: dict, max_bullets: int):
    """Creates a bullet toward the mouse when the fire action is active."""
    bullet_count = sum(1 for _ in world.get_component(CTagBullet))
    if bullet_count >= max_bullets:
        return

    for _, (_, transform, sprite, cmd) in world.get_components(
            CTagPlayer, CTransform, CSurface, CInputCommand):
        if PlayerAction.PLAYER_FIRE in cmd.actions:
            center_x = transform.x + sprite.area.width / 2
            center_y = transform.y + sprite.area.height / 2
            create_bullet(
                world,
                origin_x=center_x,
                origin_y=center_y,
                target_x=cmd.mouse_x,
                target_y=cmd.mouse_y,
                bullet_cfg=bullet_cfg,
            )
