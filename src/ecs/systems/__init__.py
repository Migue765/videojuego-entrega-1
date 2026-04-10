from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_bounce import system_bounce
from src.ecs.systems.s_rendering import system_render
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input import system_player_input
from src.ecs.systems.s_player_state import (
    system_player_movement,
    system_player_boundary,
    system_player_fire,
)
from src.ecs.systems.s_collision_enemy import (
    system_bullet_boundary,
    system_bullet_enemy_collision,
    system_player_enemy_collision,
)
