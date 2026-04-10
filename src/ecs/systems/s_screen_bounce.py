import esper

from src.ecs.components import CTransform, CVelocity, CShape, CTagEnemy


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
