import pygame
import esper

from src.ecs.components import (
    CTransform, CVelocity, CShape, CEnemySpawner,
    CInputCommand, CTagPlayer, CTagBullet, CTagEnemy, PlayerAction
)
from src.create import create_rectangle, create_bullet


# ---------------------------------------------------------------------------
# Existing systems (exercise 1)
# ---------------------------------------------------------------------------

def system_movement(world: esper.World, delta_time: float):
    """Moves all entities that have a velocity (enemies and bullets)."""
    for _, (transform, velocity) in world.get_components(CTransform, CVelocity):
        transform.x += velocity.vx * delta_time
        transform.y += velocity.vy * delta_time


def system_bounce(world: esper.World, window_w: int, window_h: int):
    """Bounces enemies off screen edges (does not affect player or bullets)."""
    for _, (transform, velocity, shape, _) in world.get_components(
            CTransform, CVelocity, CShape, CTagEnemy):
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
    """Draws all entities that have a transform and shape."""
    for _, (transform, shape) in world.get_components(CTransform, CShape):
        pygame.draw.rect(
            surface,
            (shape.r, shape.g, shape.b),
            pygame.Rect(int(transform.x), int(transform.y), shape.w, shape.h)
        )


def system_enemy_spawner(world: esper.World, delta_time: float):
    """Spawns enemies according to the level timed events."""
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


# ---------------------------------------------------------------------------
# New systems (exercise 2)
# ---------------------------------------------------------------------------

def system_player_input(world: esper.World, events: list):
    """Reads keyboard/mouse input and updates the player's CInputCommand.

    Implements the Command pattern: each frame the set of active PlayerAction
    constants is rebuilt from the current hardware state.
    """
    keys = pygame.key.get_pressed()

    for _, (_, cmd) in world.get_components(CTagPlayer, CInputCommand):
        # Rebuild movement actions every frame from key state
        cmd.actions.discard(PlayerAction.PLAYER_LEFT)
        cmd.actions.discard(PlayerAction.PLAYER_RIGHT)
        cmd.actions.discard(PlayerAction.PLAYER_UP)
        cmd.actions.discard(PlayerAction.PLAYER_DOWN)
        cmd.actions.discard(PlayerAction.PLAYER_FIRE)

        if keys[pygame.K_LEFT]:
            cmd.actions.add(PlayerAction.PLAYER_LEFT)
        if keys[pygame.K_RIGHT]:
            cmd.actions.add(PlayerAction.PLAYER_RIGHT)
        if keys[pygame.K_UP]:
            cmd.actions.add(PlayerAction.PLAYER_UP)
        if keys[pygame.K_DOWN]:
            cmd.actions.add(PlayerAction.PLAYER_DOWN)

        # Fire is triggered by a discrete mouse-button-down event
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cmd.actions.add(PlayerAction.PLAYER_FIRE)
                cmd.mouse_x, cmd.mouse_y = event.pos


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
    """Creates a bullet when the fire action is active, respecting the bullet limit."""
    # Count bullets currently alive
    bullet_count = sum(1 for _ in world.get_component(CTagBullet))
    if bullet_count >= max_bullets:
        return

    for _, (_, transform, shape, cmd) in world.get_components(
            CTagPlayer, CTransform, CShape, CInputCommand):
        if PlayerAction.PLAYER_FIRE in cmd.actions:
            center_x = transform.x + shape.w / 2
            center_y = transform.y + shape.h / 2
            bw = bullet_cfg["size"]["w"]
            bh = bullet_cfg["size"]["h"]
            bc = (
                bullet_cfg["color"]["r"],
                bullet_cfg["color"]["g"],
                bullet_cfg["color"]["b"]
            )
            bs = bullet_cfg["speed"]
            create_bullet(
                world,
                origin_x=center_x,
                origin_y=center_y,
                target_x=cmd.mouse_x,
                target_y=cmd.mouse_y,
                w=bw, h=bh,
                color=bc,
                speed=bs
            )


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
