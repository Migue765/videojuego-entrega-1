from dataclasses import dataclass, field


@dataclass
class SpawnEvent:
    time: float
    enemy_type: str
    x: float
    y: float
    triggered: bool = False


@dataclass
class CEnemySpawner:
    events: list = field(default_factory=list)
    enemies_data: dict = field(default_factory=dict)
    elapsed: float = 0.0
