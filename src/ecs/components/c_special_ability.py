from dataclasses import dataclass


@dataclass
class CSpecialAbility:
    """Tracks the shield-pulse cooldown for the player special ability."""

    cooldown_max: float = 5.0
    cooldown_remaining: float = 0.0
    radius: float = 200.0

    @property
    def is_ready(self) -> bool:
        return self.cooldown_remaining <= 0.0
