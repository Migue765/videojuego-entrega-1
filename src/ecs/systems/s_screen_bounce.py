import esper

from src.ecs.components import CTransform, CVelocity, CSurface, CTagEnemy, CTagHunter


def system_bounce(world: esper.World, window_w: int, window_h: int):
    """Bounces non-hunter enemies off screen edges."""
    hunters = {ent for ent, _ in world.get_component(CTagHunter)}
    for ent, (transform, velocity, sprite, _) in world.get_components(
            CTransform, CVelocity, CSurface, CTagEnemy):
        if ent in hunters:
            continue
        w = sprite.area.width
        h = sprite.area.height
        if transform.x < 0:
            transform.x = 0
            velocity.vx = abs(velocity.vx)
        elif transform.x + w > window_w:
            transform.x = window_w - w
            velocity.vx = -abs(velocity.vx)

        if transform.y < 0:
            transform.y = 0
            velocity.vy = abs(velocity.vy)
        elif transform.y + h > window_h:
            transform.y = window_h - h
            velocity.vy = -abs(velocity.vy)
