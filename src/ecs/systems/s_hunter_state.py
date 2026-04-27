import math

import esper

from src.ecs.components import (
    CTransform, CVelocity, CSurface, CAnimation,
    CHunterState, HUNTER_IDLE, HUNTER_CHASING, HUNTER_RETURNING,
    CTagPlayer, CTagHunter,
)


def _player_center(world: esper.World):
    for _, (_, tf, sp) in world.get_components(CTagPlayer, CTransform, CSurface):
        return tf.x + sp.area.width / 2, tf.y + sp.area.height / 2
    return None


def system_hunter_state(world: esper.World):
    """Drives the Hunter AI. Transitions between IDLE, CHASING and RETURNING.

    - IDLE: stopped at origin. If player is within `chase_distance` → CHASING.
    - CHASING: moves toward the player at `chase_speed`. If the hunter gets
      farther than `return_distance` from its origin, switches to RETURNING.
    - RETURNING: moves back toward the origin at `return_speed`. Upon reaching
      the origin, returns to IDLE and may chase again.
    """
    player = _player_center(world)

    for _, (_, state, transform, velocity, sprite, anim) in world.get_components(
            CTagHunter, CHunterState, CTransform, CVelocity, CSurface, CAnimation):
        cx = transform.x + sprite.area.width / 2
        cy = transform.y + sprite.area.height / 2
        ox = state.origin_x + sprite.area.width / 2
        oy = state.origin_y + sprite.area.height / 2

        dist_origin = math.hypot(cx - ox, cy - oy)

        if state.state == HUNTER_RETURNING:
            dx = ox - cx
            dy = oy - cy
            d = math.hypot(dx, dy)
            if d <= max(state.return_speed * 0.02, 1.0):
                transform.x = state.origin_x
                transform.y = state.origin_y
                velocity.vx = 0.0
                velocity.vy = 0.0
                state.state = HUNTER_IDLE
                anim.play("IDLE")
            else:
                velocity.vx = (dx / d) * state.return_speed
                velocity.vy = (dy / d) * state.return_speed
                anim.play("MOVE")
            continue

        if dist_origin > state.return_distance:
            state.state = HUNTER_RETURNING
            anim.play("MOVE")
            continue

        if player is None:
            velocity.vx = 0.0
            velocity.vy = 0.0
            state.state = HUNTER_IDLE
            anim.play("IDLE")
            continue

        px, py = player
        dx = px - cx
        dy = py - cy
        dist_player = math.hypot(dx, dy)

        if state.state == HUNTER_IDLE:
            if dist_player <= state.chase_distance:
                state.state = HUNTER_CHASING
                if state.sound_chase:
                    from src.engine.service_locator import ServiceLocator
                    ServiceLocator.sounds().play(state.sound_chase)
            else:
                velocity.vx = 0.0
                velocity.vy = 0.0
                anim.play("IDLE")
                continue

        if state.state == HUNTER_CHASING:
            if dist_player == 0:
                velocity.vx = 0.0
                velocity.vy = 0.0
            else:
                velocity.vx = (dx / dist_player) * state.chase_speed
                velocity.vy = (dy / dist_player) * state.chase_speed
            anim.play("MOVE")
