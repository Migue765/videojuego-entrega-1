import esper

from src.ecs.components import CTransform, CVelocity


def system_movement(world: esper.World, delta_time: float):
    """Moves all entities that have a velocity (enemies and bullets)."""
    for _, (transform, velocity) in world.get_components(CTransform, CVelocity):
        transform.x += velocity.vx * delta_time
        transform.y += velocity.vy * delta_time
