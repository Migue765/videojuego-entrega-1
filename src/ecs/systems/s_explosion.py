import esper

from src.ecs.components import CAnimation, CTagExplosion


def system_explosion(world: esper.World):
    """Deletes explosion entities once their animation has finished."""
    to_delete = []
    for ent, (_, anim) in world.get_components(CTagExplosion, CAnimation):
        if anim.finished:
            to_delete.append(ent)
    for ent in to_delete:
        world.delete_entity(ent, immediate=True)
