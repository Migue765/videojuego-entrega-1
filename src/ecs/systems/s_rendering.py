import pygame
import esper

from src.ecs.components import CTransform, CSurface


def system_render(world: esper.World, surface: pygame.Surface):
    """Draws all entities that have a transform and a surface (texture/sprite)."""
    for _, (transform, sprite) in world.get_components(CTransform, CSurface):
        if sprite.surf is None:
            continue
        surface.blit(sprite.surf, (int(transform.x), int(transform.y)), sprite.area)
