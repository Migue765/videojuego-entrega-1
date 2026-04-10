import pygame
import esper

from src.ecs.components import CInputCommand, CTagPlayer
from src.ecs.commands import PlayerAction


def system_player_input(world: esper.World, events: list):
    """Reads keyboard/mouse input and updates the player's CInputCommand.

    Implementa el patrón Command: cada frame se reconstruye el conjunto de
    acciones activas (PlayerAction) a partir del estado actual del hardware.
    """
    keys = pygame.key.get_pressed()

    for _, (_, cmd) in world.get_components(CTagPlayer, CInputCommand):
        cmd.actions.discard(PlayerAction.PLAYER_LEFT)
        cmd.actions.discard(PlayerAction.PLAYER_RIGHT)
        cmd.actions.discard(PlayerAction.PLAYER_UP)
        cmd.actions.discard(PlayerAction.PLAYER_DOWN)
        cmd.actions.discard(PlayerAction.PLAYER_FIRE)

        if keys[pygame.K_LEFT]:
            cmd.actions.add(PlayerAction.PLAYER_LEFT)
        if keys[pygame.K_RIGHT]:
            cmd.actions.add(PlayerAction.PLAYER_RIGHT)
        if keys[pygame.K_UP]:
            cmd.actions.add(PlayerAction.PLAYER_UP)
        if keys[pygame.K_DOWN]:
            cmd.actions.add(PlayerAction.PLAYER_DOWN)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cmd.actions.add(PlayerAction.PLAYER_FIRE)
                cmd.mouse_x, cmd.mouse_y = event.pos
