import esper

from src.ecs.components import CAnimation, CSurface


def system_animation(world: esper.World, delta_time: float):
    """Advances the animation frame for every entity that has CAnimation + CSurface.

    Updates the CSurface.area to point at the current frame inside the sprite sheet.
    Single-frame animations stay on the start frame. For multi-frame animations it
    loops; the `finished` flag is raised once the last frame is reached so other
    systems (e.g., explosion cleanup) can react.
    """
    for _, (anim, sprite) in world.get_components(CAnimation, CSurface):
        active = anim.active()
        num_animation_frames = active.num_frames()

        if num_animation_frames > 1:
            anim.current_frame += active.framerate * delta_time
            if anim.current_frame >= active.end + 1:
                anim.finished = True
                anim.current_frame = active.start + (anim.current_frame - active.start) % num_animation_frames

        frame_index = int(anim.current_frame)
        frame_w = sprite.surf.get_width() // max(anim.number_frames, 1)
        sprite.area.x = frame_index * frame_w
        sprite.area.y = 0
        sprite.area.width = frame_w
        sprite.area.height = sprite.surf.get_height()
