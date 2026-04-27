"""Service Locator pattern: centralised registry for image, sound and font services."""
import pygame


class _ImageService:
    """Loads and caches pygame Surfaces keyed by (path, num_frames)."""

    def __init__(self) -> None:
        self._cache: dict = {}

    def get(self, path: str, num_frames: int = 1):
        from src.ecs.components.c_surface import CSurface
        key = (path, num_frames)
        if key not in self._cache:
            self._cache[key] = pygame.image.load(path).convert_alpha()
        surf = self._cache[key]
        frame_w = surf.get_width() // max(num_frames, 1)
        return CSurface(surf=surf, area=pygame.Rect(0, 0, frame_w, surf.get_height()))


class _SoundService:
    """Loads, caches and plays pygame Sound objects."""

    def __init__(self) -> None:
        self._cache: dict = {}

    def get(self, path: str) -> pygame.mixer.Sound:
        if path not in self._cache:
            self._cache[path] = pygame.mixer.Sound(path)
        return self._cache[path]

    def play(self, path: str) -> None:
        if not path:
            return
        try:
            self.get(path).play()
        except Exception:
            pass


class _FontService:
    """Loads and caches pygame Font objects keyed by (path, size)."""

    def __init__(self) -> None:
        self._cache: dict = {}

    def get(self, path: str, size: int) -> pygame.font.Font:
        key = (path, size)
        if key not in self._cache:
            self._cache[key] = pygame.font.Font(path, size)
        return self._cache[key]


class ServiceLocator:
    """Singleton registry that provides access to engine services."""

    _images: _ImageService = None
    _sounds: _SoundService = None
    _fonts: _FontService = None

    @classmethod
    def initialize(cls) -> None:
        cls._images = _ImageService()
        cls._sounds = _SoundService()
        cls._fonts = _FontService()

    @classmethod
    def images(cls) -> _ImageService:
        return cls._images

    @classmethod
    def sounds(cls) -> _SoundService:
        return cls._sounds

    @classmethod
    def fonts(cls) -> _FontService:
        return cls._fonts
