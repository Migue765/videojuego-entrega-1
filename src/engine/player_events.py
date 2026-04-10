import esper

from src.ecs.systems import (
    system_player_input,
    system_player_movement,
    system_player_boundary,
    system_player_fire,
    system_player_enemy_collision,
)


def process_player_events(
    world: esper.World,
    events: list,
    delta_time: float,
    player_cfg: dict,
    bullet_cfg: dict,
    max_bullets: int,
    window_w: int,
    window_h: int,
) -> None:
    """Agrupa todos los sistemas relacionados con el jugador en cada frame."""
    system_player_input(world, events)
    system_player_movement(world, delta_time, player_cfg["speed"])
    system_player_boundary(world, window_w, window_h)
    system_player_fire(world, bullet_cfg, max_bullets)
    system_player_enemy_collision(world)
