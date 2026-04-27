import math
import random

import esper

from src.ecs.components import (
    CTransform, CVelocity, CSurface, CAnimation, CHunterState,
    CEnemySpawner, SpawnEvent,
    CTagPlayer, CTagBullet, CTagEnemy, CTagHunter, CTagExplosion,
    CInputCommand, CSpecialAbility,
)
from src.engine.service_locator import ServiceLocator


def _load_surface(image_path: str, number_frames: int = 1) -> CSurface:
    return ServiceLocator.images().get(image_path, number_frames)


def create_enemy(world: esper.World, x: float, y: float, enemy_data: dict) -> int:
    """Creates a static-sprite asteroid-type enemy with a random velocity."""
    surface_cmp = _load_surface(enemy_data["image"], number_frames=1)

    speed = random.uniform(enemy_data["velocity_min"], enemy_data["velocity_max"])
    angle = random.uniform(0, 2 * math.pi)
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)

    ServiceLocator.sounds().play(enemy_data.get("sound", ""))

    entity = world.create_entity()
    world.add_component(entity, CTransform(x=x - surface_cmp.area.width / 2,
                                           y=y - surface_cmp.area.height / 2))
    world.add_component(entity, CVelocity(vx=vx, vy=vy))
    world.add_component(entity, surface_cmp)
    world.add_component(entity, CTagEnemy())
    return entity


def create_hunter(world: esper.World, x: float, y: float, enemy_data: dict) -> int:
    """Creates the Hunter enemy: animated, chases player within range, returns to origin."""
    animations_cfg = enemy_data["animations"]
    number_frames = int(animations_cfg.get("number_frames", 1))
    surface_cmp = _load_surface(enemy_data["image"], number_frames=number_frames)
    anim_cmp = CAnimation.from_config(animations_cfg)

    tx = x - surface_cmp.area.width / 2
    ty = y - surface_cmp.area.height / 2

    entity = world.create_entity()
    world.add_component(entity, CTransform(x=tx, y=ty))
    world.add_component(entity, CVelocity(vx=0.0, vy=0.0))
    world.add_component(entity, surface_cmp)
    world.add_component(entity, anim_cmp)
    world.add_component(entity, CHunterState(
        origin_x=tx,
        origin_y=ty,
        chase_distance=float(enemy_data["distance_start_chase"]),
        return_distance=float(enemy_data["distance_start_return"]),
        chase_speed=float(enemy_data["velocity_chase"]),
        return_speed=float(enemy_data.get("velocity_return", enemy_data["velocity_chase"])),
        sound_chase=enemy_data.get("sound_chase", ""),
    ))
    world.add_component(entity, CTagEnemy())
    world.add_component(entity, CTagHunter())
    return entity


def create_enemy_spawner(world: esper.World, level_data: dict, enemies_data: dict) -> int:
    events = []
    for ev in level_data.get("enemy_spawn_events", []):
        events.append(SpawnEvent(
            time=ev["time"],
            enemy_type=ev["enemy_type"],
            x=ev["position"]["x"],
            y=ev["position"]["y"],
        ))
    spawner = CEnemySpawner(events=events, enemies_data=enemies_data)
    entity = world.create_entity()
    world.add_component(entity, spawner)
    return entity


def create_player(world: esper.World, x: float, y: float, player_cfg: dict) -> int:
    """Creates the animated player entity with special ability component."""
    animations_cfg = player_cfg["animations"]
    number_frames = int(animations_cfg.get("number_frames", 1))
    surface_cmp = _load_surface(player_cfg["image"], number_frames=number_frames)
    anim_cmp = CAnimation.from_config(animations_cfg)
    anim_cmp.play("IDLE")

    special_cfg = player_cfg.get("special_ability", {})
    ability = CSpecialAbility(
        cooldown_max=float(special_cfg.get("cooldown", 5.0)),
        radius=float(special_cfg.get("radius", 200.0)),
    )

    entity = world.create_entity()
    world.add_component(entity, CTransform(
        x=x - surface_cmp.area.width / 2,
        y=y - surface_cmp.area.height / 2,
    ))
    world.add_component(entity, surface_cmp)
    world.add_component(entity, anim_cmp)
    world.add_component(entity, CTagPlayer())
    world.add_component(entity, CInputCommand())
    world.add_component(entity, ability)
    return entity


def create_bullet(world: esper.World, origin_x: float, origin_y: float,
                  target_x: float, target_y: float, bullet_cfg: dict):
    """Creates a bullet fired from the player center toward the mouse position."""
    dx = target_x - origin_x
    dy = target_y - origin_y
    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0:
        return None

    speed = float(bullet_cfg.get("velocity", bullet_cfg.get("speed", 0)))
    vx = (dx / dist) * speed
    vy = (dy / dist) * speed

    ServiceLocator.sounds().play(bullet_cfg.get("sound", ""))

    surface_cmp = _load_surface(bullet_cfg["image"], number_frames=1)

    entity = world.create_entity()
    world.add_component(entity, CTransform(
        x=origin_x - surface_cmp.area.width / 2,
        y=origin_y - surface_cmp.area.height / 2,
    ))
    world.add_component(entity, CVelocity(vx=vx, vy=vy))
    world.add_component(entity, surface_cmp)
    world.add_component(entity, CTagBullet())
    return entity


def create_explosion(world: esper.World, center_x: float, center_y: float,
                     explosion_cfg: dict) -> int:
    """Creates an explosion entity centered at (center_x, center_y)."""
    animations_cfg = explosion_cfg["animations"]
    number_frames = int(animations_cfg.get("number_frames", 1))
    surface_cmp = _load_surface(explosion_cfg["image"], number_frames=number_frames)
    anim_cmp = CAnimation.from_config(animations_cfg)

    ServiceLocator.sounds().play(explosion_cfg.get("sound", ""))

    entity = world.create_entity()
    world.add_component(entity, CTransform(
        x=center_x - surface_cmp.area.width / 2,
        y=center_y - surface_cmp.area.height / 2,
    ))
    world.add_component(entity, surface_cmp)
    world.add_component(entity, anim_cmp)
    world.add_component(entity, CTagExplosion())
    return entity
