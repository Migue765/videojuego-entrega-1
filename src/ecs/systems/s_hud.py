import pygame
import esper

from src.ecs.components import CSpecialAbility
from src.engine.service_locator import ServiceLocator


def _blit_text(screen: pygame.Surface, cfg: dict, override_text: str = None,
               override_color: tuple = None) -> None:
    """Renders a single text config entry onto the screen."""
    font = ServiceLocator.fonts().get(cfg["font"], cfg["size"])
    text = override_text if override_text is not None else cfg["text"]
    color = override_color if override_color is not None else tuple(cfg["color"])
    surf = font.render(text, True, color)
    x, y = cfg["position"]
    align = cfg.get("align", "left")
    if align == "center":
        x -= surf.get_width() // 2
    elif align == "right":
        x -= surf.get_width()
    screen.blit(surf, (int(x), int(y)))


def system_hud_render(screen: pygame.Surface, world: esper.World,
                      interface_cfg: dict) -> None:
    """Draws the game HUD: title, instructions, and dynamic shield indicator."""
    _blit_text(screen, interface_cfg["title"])
    _blit_text(screen, interface_cfg["instructions"])

    cooldown = 0.0
    for _, ability in world.get_component(CSpecialAbility):
        cooldown = ability.cooldown_remaining
        break

    shield_cfg = interface_cfg["shield_label"]
    if cooldown <= 0:
        _blit_text(screen, shield_cfg,
                   override_text="SHIELD: READY",
                   override_color=(80, 220, 120))
    else:
        _blit_text(screen, shield_cfg,
                   override_text=f"SHIELD: {cooldown:.1f}s",
                   override_color=(255, 100, 80))


def system_hud_game_over(screen: pygame.Surface, interface_cfg: dict) -> None:
    """Draws a semi-transparent game-over overlay."""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    _blit_text(screen, interface_cfg["game_over"])
    _blit_text(screen, interface_cfg["game_over_sub"])


def system_hud_pause(screen: pygame.Surface, interface_cfg: dict) -> None:
    """Draws a semi-transparent pause overlay with pause text."""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    _blit_text(screen, interface_cfg["pause"])
    _blit_text(screen, interface_cfg["pause_sub"])
