from dataclasses import dataclass, field


@dataclass
class CTransform:
    x: float = 0.0
    y: float = 0.0


@dataclass
class CVelocity:
    vx: float = 0.0
    vy: float = 0.0


@dataclass
class CShape:
    w: int = 0
    h: int = 0
    r: int = 255
    g: int = 255
    b: int = 255


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
