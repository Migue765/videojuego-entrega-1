import math

import pygame
import esper

from src.ecs.components import (
    CTransform, CSurface, CTagEnemy, CTagPlayer,
    CInputCommand, CSpecialAbility, CShieldWave,
)
from src.ecs.commands import PlayerAction
from src.engine.service_locator import ServiceLocator


def system_shield_activate(world: esper.World, explosion_cfg: dict):
    """Activates the shield pulse when player presses SPACE and ability is ready.

    - Instantly destroys all enemies within the ability radius.
    - Spawns a CShieldWave visual entity centered on the player.
    - Starts the cooldown timer.
    """
    for _, (_, tf, sp, cmd, ability) in world.get_components(
            CTagPlayer, CTransform, CSurface, CInputCommand, CSpecialAbility):
        if PlayerAction.PLAYER_SHIELD not in cmd.actions:
            continue
        cmd.actions.discard(PlayerAction.PLAYER_SHIELD)
        if not ability.is_ready:
            continue

        cx = tf.x + sp.area.width / 2
        cy = tf.y + sp.area.height / 2
        ability.cooldown_remaining = ability.cooldown_max

        # Destroy enemies inside radius and spawn explosions
        from src.create import create_explosion
        to_delete = []
        explosions = []
        for e_ent, (_, e_tf, e_sp) in world.get_components(CTagEnemy, CTransform, CSurface):
            ecx = e_tf.x + e_sp.area.width / 2
            ecy = e_tf.y + e_sp.area.height / 2
            if math.hypot(ecx - cx, ecy - cy) <= ability.radius:
                to_delete.append(e_ent)
                explosions.append((int(ecx), int(ecy)))

        for ent in to_delete:
            world.delete_entity(ent, immediate=True)
        for ecx, ecy in explosions:
            create_explosion(world, ecx, ecy, explosion_cfg)
            ServiceLocator.sounds().play(explosion_cfg.get("sound", ""))

        # Spawn visual expanding ring
        wave_ent = world.create_entity()
        world.add_component(wave_ent, CShieldWave(
            x=cx, y=cy,
            max_radius=ability.radius,
        ))
        break


def system_shield_update(world: esper.World, delta_time: float):
    """Expands the shield wave ring and removes it when fully expanded."""
    to_delete = []
    for ent, wave in world.get_component(CShieldWave):
        wave.radius += wave.expand_speed * delta_time
        fade = 1.0 - (wave.radius / wave.max_radius)
        wave.alpha = max(0, int(220 * fade))
        if wave.radius >= wave.max_radius:
            to_delete.append(ent)
    for ent in to_delete:
        world.delete_entity(ent, immediate=True)


def system_shield_cooldown(world: esper.World, delta_time: float):
    """Ticks down the shield ability cooldown each frame."""
    for _, ability in world.get_component(CSpecialAbility):
        if ability.cooldown_remaining > 0:
            ability.cooldown_remaining = max(0.0, ability.cooldown_remaining - delta_time)


def system_shield_render(world: esper.World, screen: pygame.Surface):
    """Draws the expanding cyan ring on screen using SRCALPHA blitting."""
    for _, wave in world.get_component(CShieldWave):
        if wave.alpha <= 0 or wave.radius <= 1:
            continue
        diameter = int(wave.radius * 2) + 6
        ring_surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = diameter // 2
        pygame.draw.circle(
            ring_surf,
            (wave.color_r, wave.color_g, wave.color_b, wave.alpha),
            (center, center),
            int(wave.radius),
            3,
        )
        # Inner glow (thinner, slightly different color)
        if wave.radius > 8:
            pygame.draw.circle(
                ring_surf,
                (200, 240, 255, wave.alpha // 2),
                (center, center),
                max(1, int(wave.radius) - 6),
                1,
            )
        screen.blit(ring_surf, (int(wave.x) - center, int(wave.y) - center))
