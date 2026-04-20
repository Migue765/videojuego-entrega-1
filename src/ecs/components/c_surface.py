from dataclasses import dataclass, field

import pygame


@dataclass
class CSurface:
    surf: pygame.Surface = None
    area: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))

    @classmethod
    def from_path(cls, image_path: str, num_frames: int = 1) -> "CSurface":
        surface = pygame.image.load(image_path).convert_alpha()
        frame_w = surface.get_width() // max(num_frames, 1)
        frame_h = surface.get_height()
        area = pygame.Rect(0, 0, frame_w, frame_h)
        return cls(surf=surface, area=area)
