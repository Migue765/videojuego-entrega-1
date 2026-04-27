from dataclasses import dataclass, field

import pygame


@dataclass
class CSurface:
    surf: pygame.Surface = None
    area: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))

    @classmethod
    def from_path(cls, image_path: str, num_frames: int = 1) -> "CSurface":
        from src.engine.service_locator import ServiceLocator
        return ServiceLocator.images().get(image_path, num_frames)

    @classmethod
    def from_text(cls, text: str, font: pygame.font.Font, color: tuple) -> "CSurface":
        """Creates a CSurface from rendered text. Useful for static labels."""
        surf = font.render(text, True, color)
        return cls(surf=surf, area=surf.get_rect())
