import pygame
import esper

from src.ecs.components import (
    CTransform, CSurface, CTagPlayer, CTagBullet, CTagEnemy,
)
from src.create import create_explosion


def system_bullet_boundary(world: esper.World, window_w: int, window_h: int):
    """Removes bullets that have left the screen."""
    to_delete = []
    for ent, (_, transform, sprite) in world.get_components(CTagBullet, CTransform, CSurface):
        w, h = sprite.area.width, sprite.area.height
        if (transform.x + w < 0 or transform.x > window_w or
                transform.y + h < 0 or transform.y > window_h):
            to_delete.append(ent)
    for ent in to_delete:
        world.delete_entity(ent, immediate=True)


def _entity_rect(transform: CTransform, sprite: CSurface) -> pygame.Rect:
    return pygame.Rect(int(transform.x), int(transform.y),
                       sprite.area.width, sprite.area.height)


def system_bullet_enemy_collision(world: esper.World, explosion_cfg: dict):
    """Destroys a bullet and the enemy it hits on contact, spawning an explosion."""
    bullets = list(world.get_components(CTagBullet, CTransform, CSurface))
    enemies = list(world.get_components(CTagEnemy, CTransform, CSurface))

    to_delete = set()
    explosions = []
    for b_ent, (_, b_tf, b_sp) in bullets:
        b_rect = _entity_rect(b_tf, b_sp)
        for e_ent, (_, e_tf, e_sp) in enemies:
            if e_ent in to_delete:
                continue
            e_rect = _entity_rect(e_tf, e_sp)
            if b_rect.colliderect(e_rect):
                to_delete.add(b_ent)
                to_delete.add(e_ent)
                explosions.append((e_rect.centerx, e_rect.centery))
                break

    for ent in to_delete:
        world.delete_entity(ent, immediate=True)
    for cx, cy in explosions:
        create_explosion(world, cx, cy, explosion_cfg)


def system_player_enemy_collision(world: esper.World, explosion_cfg: dict) -> bool:
    """Destroys player and enemy on contact, spawning an explosion at the player.

    Returns True if the player was killed this frame.
    """
    players = list(world.get_components(CTagPlayer, CTransform, CSurface))
    enemies = list(world.get_components(CTagEnemy, CTransform, CSurface))

    for p_ent, (_, p_tf, p_sp) in players:
        p_rect = _entity_rect(p_tf, p_sp)
        for e_ent, (_, e_tf, e_sp) in enemies:
            e_rect = _entity_rect(e_tf, e_sp)
            if p_rect.colliderect(e_rect):
                create_explosion(world, p_rect.centerx, p_rect.centery, explosion_cfg)
                create_explosion(world, e_rect.centerx, e_rect.centery, explosion_cfg)
                world.delete_entity(p_ent, immediate=True)
                world.delete_entity(e_ent, immediate=True)
                return True
    return False
