from dataclasses import dataclass, field


@dataclass
class CInputCommand:
    """Almacena las acciones activas del jugador en el frame actual (patrón Command)."""
    actions: set = field(default_factory=set)
    mouse_x: int = 0
    mouse_y: int = 0
