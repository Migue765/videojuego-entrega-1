"""Genera screenshots y cover para itch.io en modo headless."""

import os
import sys
import math
import random

# Headless mode – must be set before importing pygame
os.environ["SDL_AUDIODRIVER"] = "dummy"

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")

import pygame

# ── helpers ──────────────────────────────────────────────────────────────────

def _stars(surf, n=120):
    w, h = surf.get_size()
    rng = random.Random(42)
    for _ in range(n):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        bright = rng.randint(80, 220)
        r = rng.choice([1, 1, 1, 2])
        pygame.draw.circle(surf, (bright, bright, bright + 20), (x, y), r)


def _draw_game_frame(surf, font_small):
    """Simulates a believable game frame (no engine needed)."""
    surf.fill((25, 25, 25))
    _stars(surf, 80)

    # HUD title
    t = font_small.render("STAR DEFENDER", True, (220, 220, 255))
    surf.blit(t, (surf.get_width() // 2 - t.get_width() // 2, 10))

    # Shield label
    s = font_small.render("SHIELD: READY", True, (80, 220, 120))
    surf.blit(s, (5, 5))

    # Instructions
    ins = font_small.render("ARROWS:MOVE  CLICK:FIRE  SPACE:SHIELD  P:PAUSE", True, (120, 120, 120))
    surf.blit(ins, (surf.get_width() // 2 - ins.get_width() // 2, 350))

    return surf


def _load_img(path, scale=None):
    # Load without convert_alpha – works without a real display window
    img = pygame.image.load(path)
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    pygame.font.init()
    # No real display needed – we render to off-screen Surface objects and save directly.

    OUT = "SEMANA_4"
    os.makedirs(OUT, exist_ok=True)

    W, H = 640, 360
    CW, CH = 630, 500  # cover size required by itch.io

    font_tiny  = pygame.font.Font("assets/fnt/PressStart2P.ttf", 6)
    font_small = pygame.font.Font("assets/fnt/PressStart2P.ttf", 8)
    font_med   = pygame.font.Font("assets/fnt/PressStart2P.ttf", 14)
    font_big   = pygame.font.Font("assets/fnt/PressStart2P.ttf", 22)

    # Load sprites
    player_img   = _load_img("assets/img/player.png")
    asteroid_img = _load_img("assets/img/asteroid_01.png")
    asteroid2    = _load_img("assets/img/asteroid_02.png")
    asteroid3    = _load_img("assets/img/asteroid_03.png")
    bullet_img   = _load_img("assets/img/bullet.png")
    enemy_img    = _load_img("assets/img/enemy.png")
    expl_img     = _load_img("assets/img/explosion.png")

    # player sprite (first frame)
    pf_w = player_img.get_width() // 4
    player_frame = pygame.Surface((pf_w, player_img.get_height()), pygame.SRCALPHA)
    player_frame.blit(player_img, (0, 0), (0, 0, pf_w, player_img.get_height()))

    # enemy sprite (first frame)
    ef_w = enemy_img.get_width() // 6
    enemy_frame = pygame.Surface((ef_w, enemy_img.get_height()), pygame.SRCALPHA)
    enemy_frame.blit(enemy_img, (0, 0), (0, 0, ef_w, enemy_img.get_height()))

    # explosion sprite (third frame)
    xf_w = expl_img.get_width() // 8
    expl_frame = pygame.Surface((xf_w, expl_img.get_height()), pygame.SRCALPHA)
    expl_frame.blit(expl_img, (0, 0), (2 * xf_w, 0, xf_w, expl_img.get_height()))

    # ── screenshot 1 : normal gameplay ────────────────────────────────────────
    s1 = pygame.Surface((W, H))
    s1.fill((25, 25, 25))
    _stars(s1, 80)

    s1.blit(asteroid_img, (60, 40))
    s1.blit(asteroid2, (480, 200))
    s1.blit(asteroid3, (200, 280))
    s1.blit(enemy_frame, (520, 160))
    s1.blit(enemy_frame, (30, 160))
    s1.blit(player_frame, (310, 165))
    s1.blit(bullet_img, (380, 155))
    s1.blit(bullet_img, (415, 140))

    s1.blit(font_med.render("STAR DEFENDER", True, (220, 220, 255)),
            (W // 2 - font_med.render("STAR DEFENDER", True, (0,0,0)).get_width() // 2, 10))
    s1.blit(font_small.render("SHIELD: READY", True, (80, 220, 120)), (5, 5))
    s1.blit(font_tiny.render("ARROWS:MOVE  CLICK:FIRE  SPACE:SHIELD  P:PAUSE",
                             True, (120, 120, 120)),
            (W // 2 - 190, 350))

    pygame.image.save(s1, f"{OUT}/screenshot_gameplay.png")
    print("saved screenshot_gameplay.png")

    # ── screenshot 2 : shield pulse active ────────────────────────────────────
    s2 = s1.copy()

    # shield ring
    for radius in range(20, 185, 30):
        alpha = max(0, 220 - radius)
        ring = pygame.Surface((radius * 2 + 6, radius * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(ring, (80, 200, 255, alpha),
                           (radius + 3, radius + 3), radius, 3)
        cx, cy = 320 + pf_w // 2, 165 + player_frame.get_height() // 2
        s2.blit(ring, (cx - radius - 3, cy - radius - 3))

    # cooldown text
    s2.blit(font_small.render("SHIELD: 4.8s", True, (255, 100, 80)), (5, 5))

    # flash overlay
    flash = pygame.Surface((W, H), pygame.SRCALPHA)
    flash.fill((80, 200, 255, 25))
    s2.blit(flash, (0, 0))

    pygame.image.save(s2, f"{OUT}/screenshot_shield.png")
    print("saved screenshot_shield.png")

    # ── screenshot 3 : bullets in flight ──────────────────────────────────────
    s3 = pygame.Surface((W, H))
    s3.fill((25, 25, 25))
    _stars(s3, 80)

    s3.blit(asteroid_img, (90, 80))
    s3.blit(asteroid2, (430, 240))
    s3.blit(enemy_frame, (550, 140))
    s3.blit(player_frame, (280, 165))
    # salvo of bullets
    for bx, by in [(320, 150), (355, 130), (390, 110), (295, 145), (270, 120)]:
        s3.blit(bullet_img, (bx, by))
    s3.blit(font_med.render("STAR DEFENDER", True, (220, 220, 255)),
            (W // 2 - 100, 10))
    s3.blit(font_small.render("SHIELD: READY", True, (80, 220, 120)), (5, 5))
    s3.blit(font_tiny.render("ARROWS:MOVE  CLICK:FIRE  SPACE:SHIELD  P:PAUSE",
                             True, (120, 120, 120)),
            (W // 2 - 190, 350))

    pygame.image.save(s3, f"{OUT}/screenshot_bullets.png")
    print("saved screenshot_bullets.png")

    # ── screenshot 4 : pause screen ───────────────────────────────────────────
    s4 = s1.copy()
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    s4.blit(overlay, (0, 0))

    pause_txt  = font_big.render("- PAUSED -", True, (255, 220, 0))
    resume_txt = font_small.render("Press P to resume", True, (200, 200, 200))
    s4.blit(pause_txt,  (W // 2 - pause_txt.get_width() // 2, 150))
    s4.blit(resume_txt, (W // 2 - resume_txt.get_width() // 2, 195))

    pygame.image.save(s4, f"{OUT}/screenshot_pause.png")
    print("saved screenshot_pause.png")

    # ── cover 630×500 ─────────────────────────────────────────────────────────
    cover = pygame.Surface((CW, CH))
    cover.fill((10, 10, 20))
    _stars(cover, 180)

    # gradient top bar
    for y in range(80):
        alpha = int(80 * (1 - y / 80))
        pygame.draw.line(cover, (40, 40, 80 + alpha), (0, y), (CW, y))

    # title
    title1 = font_big.render("STAR", True, (220, 230, 255))
    title2 = font_big.render("DEFENDER", True, (100, 180, 255))
    cover.blit(title1, (CW // 2 - title1.get_width() // 2, 18))
    cover.blit(title2, (CW // 2 - title2.get_width() // 2, 52))

    # game frame embedded (scaled up a bit and framed)
    frame_w, frame_h = 580, 326
    game_frame = pygame.transform.smoothscale(s1, (frame_w, frame_h))
    fx = (CW - frame_w) // 2
    fy = 100

    # border glow
    glow = pygame.Surface((frame_w + 8, frame_h + 8), pygame.SRCALPHA)
    glow.fill((0, 0, 0, 0))
    pygame.draw.rect(glow, (100, 180, 255, 120), glow.get_rect(), 4)
    cover.blit(glow, (fx - 4, fy - 4))
    cover.blit(game_frame, (fx, fy))

    # tagline + controls
    tag = font_small.render("Survive the asteroid storm!", True, (180, 200, 255))
    cover.blit(tag, (CW // 2 - tag.get_width() // 2, fy + frame_h + 12))

    ctrl = font_tiny.render(
        "ARROWS: Move   LMB: Fire   SPACE: Shield Pulse   P: Pause",
        True, (130, 130, 160))
    cover.blit(ctrl, (CW // 2 - ctrl.get_width() // 2, fy + frame_h + 34))

    # small decorative asteroids bottom-right
    cover.blit(pygame.transform.scale(asteroid_img, (28, 28)), (CW - 60, CH - 50))
    cover.blit(pygame.transform.scale(asteroid2,   (20, 20)), (CW - 30, CH - 75))

    pygame.image.save(cover, f"{OUT}/cover.png")
    print("saved cover.png  (630x500)")

    pygame.quit()
    print("Done.")


if __name__ == "__main__":
    main()
