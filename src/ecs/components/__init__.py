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


# Tag components — identify entity types for systems
@dataclass
class CTagPlayer:
    pass


@dataclass
class CTagBullet:
    pass


@dataclass
class CTagEnemy:
    pass


# Player action constants for the Command pattern
class PlayerAction:
    PLAYER_LEFT = "PLAYER_LEFT"
    PLAYER_RIGHT = "PLAYER_RIGHT"
    PLAYER_UP = "PLAYER_UP"
    PLAYER_DOWN = "PLAYER_DOWN"
    PLAYER_FIRE = "PLAYER_FIRE"


@dataclass
class CInputCommand:
    """Stores the set of active player actions each frame (Command pattern)."""
    actions: set = field(default_factory=set)
    mouse_x: int = 0
    mouse_y: int = 0
