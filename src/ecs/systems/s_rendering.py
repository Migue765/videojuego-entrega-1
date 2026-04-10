import pygame
import esper

from src.ecs.components import CTransform, CShape


def system_render(world: esper.World, surface: pygame.Surface):
    """Draws all entities that have a transform and shape."""
    for _, (transform, shape) in world.get_components(CTransform, CShape):
        pygame.draw.rect(
            surface,
            (shape.r, shape.g, shape.b),
            pygame.Rect(int(transform.x), int(transform.y), shape.w, shape.h)
        )
