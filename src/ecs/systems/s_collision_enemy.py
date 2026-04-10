import pygame
import esper

from src.ecs.components import CTransform, CShape, CTagPlayer, CTagBullet, CTagEnemy


def system_bullet_boundary(world: esper.World, window_w: int, window_h: int):
    """Removes bullets that have left the screen."""
    to_delete = []
    for ent, (_, transform, shape) in world.get_components(CTagBullet, CTransform, CShape):
        if (transform.x + shape.w < 0 or transform.x > window_w or
                transform.y + shape.h < 0 or transform.y > window_h):
            to_delete.append(ent)
    for ent in to_delete:
        world.delete_entity(ent, immediate=True)


def system_bullet_enemy_collision(world: esper.World):
    """Destroys a bullet and the enemy it hits on contact."""
    bullets = list(world.get_components(CTagBullet, CTransform, CShape))
    enemies = list(world.get_components(CTagEnemy, CTransform, CShape))

    to_delete = set()
    for b_ent, (_, b_tf, b_sh) in bullets:
        b_rect = pygame.Rect(int(b_tf.x), int(b_tf.y), b_sh.w, b_sh.h)
        for e_ent, (_, e_tf, e_sh) in enemies:
            if e_ent in to_delete:
                continue
            e_rect = pygame.Rect(int(e_tf.x), int(e_tf.y), e_sh.w, e_sh.h)
            if b_rect.colliderect(e_rect):
                to_delete.add(b_ent)
                to_delete.add(e_ent)
                break

    for ent in to_delete:
        world.delete_entity(ent, immediate=True)


def system_player_enemy_collision(world: esper.World):
    """Destroys the player when it collides with an enemy."""
    players = list(world.get_components(CTagPlayer, CTransform, CShape))
    enemies = list(world.get_components(CTagEnemy, CTransform, CShape))

    for p_ent, (_, p_tf, p_sh) in players:
        p_rect = pygame.Rect(int(p_tf.x), int(p_tf.y), p_sh.w, p_sh.h)
        for _, (_, e_tf, e_sh) in enemies:
            e_rect = pygame.Rect(int(e_tf.x), int(e_tf.y), e_sh.w, e_sh.h)
            if p_rect.colliderect(e_rect):
                world.delete_entity(p_ent, immediate=True)
                break
