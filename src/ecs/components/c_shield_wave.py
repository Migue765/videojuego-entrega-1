from dataclasses import dataclass


@dataclass
class CShieldWave:
    """Visual expanding ring spawned when the player activates the shield pulse."""

    x: float = 0.0
    y: float = 0.0
    radius: float = 0.0
    max_radius: float = 200.0
    expand_speed: float = 500.0   # pixels per second
    alpha: int = 220
    color_r: int = 80
    color_g: int = 200
    color_b: int = 255
