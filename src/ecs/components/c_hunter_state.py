from dataclasses import dataclass


HUNTER_IDLE = "IDLE"
HUNTER_CHASING = "CHASING"
HUNTER_RETURNING = "RETURNING"


@dataclass
class CHunterState:
    origin_x: float = 0.0
    origin_y: float = 0.0
    chase_distance: float = 0.0
    return_distance: float = 0.0
    chase_speed: float = 0.0
    return_speed: float = 0.0
    state: str = HUNTER_IDLE
    sound_chase: str = ""
