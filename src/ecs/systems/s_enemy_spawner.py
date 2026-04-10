import esper

from src.ecs.components import CEnemySpawner
from src.create import create_rectangle


def system_enemy_spawner(world: esper.World, delta_time: float):
    """Spawns enemies according to the level timed events."""
    for _, spawner in world.get_component(CEnemySpawner):
        spawner.elapsed += delta_time
        for event in spawner.events:
            if not event.triggered and spawner.elapsed >= event.time:
                enemy_data = spawner.enemies_data.get(event.enemy_type)
                if enemy_data:
                    create_rectangle(
                        world,
                        x=event.x,
                        y=event.y,
                        w=enemy_data["size"]["x"],
                        h=enemy_data["size"]["y"],
                        color=(
                            enemy_data["color"]["r"],
                            enemy_data["color"]["g"],
                            enemy_data["color"]["b"]
                        ),
                        speed_min=enemy_data["velocity_min"],
                        speed_max=enemy_data["velocity_max"]
                    )
                event.triggered = True
