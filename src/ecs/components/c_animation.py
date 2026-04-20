from dataclasses import dataclass, field


@dataclass
class AnimationData:
    name: str
    start: int
    end: int
    framerate: float

    def num_frames(self) -> int:
        return self.end - self.start + 1


@dataclass
class CAnimation:
    animations: dict = field(default_factory=dict)
    number_frames: int = 1
    current_animation: str = ""
    current_frame: float = 0.0
    finished: bool = False

    @classmethod
    def from_config(cls, animations_cfg: dict) -> "CAnimation":
        animations = {}
        for item in animations_cfg.get("list", []):
            animations[item["name"]] = AnimationData(
                name=item["name"],
                start=int(item["start"]),
                end=int(item["end"]),
                framerate=float(item["framerate"]),
            )
        first = next(iter(animations.keys()), "")
        return cls(
            animations=animations,
            number_frames=int(animations_cfg.get("number_frames", 1)),
            current_animation=first,
            current_frame=float(animations[first].start) if first else 0.0,
        )

    def play(self, name: str) -> None:
        if name == self.current_animation or name not in self.animations:
            return
        self.current_animation = name
        self.current_frame = float(self.animations[name].start)
        self.finished = False

    def active(self) -> AnimationData:
        return self.animations[self.current_animation]
