import esper

from src.ecs.components import CEnemySpawner
from src.create import create_enemy, create_hunter


def system_enemy_spawner(world: esper.World, delta_time: float):
    """Spawns enemies according to the level timed events."""
    for _, spawner in world.get_component(CEnemySpawner):
        spawner.elapsed += delta_time
        for event in spawner.events:
            if event.triggered or spawner.elapsed < event.time:
                continue
            enemy_data = spawner.enemies_data.get(event.enemy_type)
            if enemy_data is not None:
                if "animations" in enemy_data and "velocity_chase" in enemy_data:
                    create_hunter(world, event.x, event.y, enemy_data)
                else:
                    create_enemy(world, event.x, event.y, enemy_data)
            event.triggered = True
