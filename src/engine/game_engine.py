import json
import os

import pygame
import esper

from src.ecs.systems import system_movement, system_bounce, system_render, system_enemy_spawner
from src.create import create_enemy_spawner


class GameEngine:
    def __init__(self) -> None:
        self.is_running = False

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        cfg_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "cfg")
        cfg_path = os.path.normpath(cfg_path)

        with open(os.path.join(cfg_path, "window.json")) as f:
            window_cfg = json.load(f)
        with open(os.path.join(cfg_path, "enemies.json")) as f:
            enemies_data = json.load(f)
        with open(os.path.join(cfg_path, "level_01.json")) as f:
            level_data = json.load(f)

        pygame.init()
        self._window_w = window_cfg["size"]["w"]
        self._window_h = window_cfg["size"]["h"]
        self._bg_color = (
            window_cfg["bg_color"]["r"],
            window_cfg["bg_color"]["g"],
            window_cfg["bg_color"]["b"]
        )
        self._screen = pygame.display.set_mode((self._window_w, self._window_h))
        pygame.display.set_caption(window_cfg["title"])
        self._clock = pygame.time.Clock()
        self._framerate = window_cfg["framerate"]
        self._delta_time = 0.0

        self._world = esper.World()
        create_enemy_spawner(self._world, level_data, enemies_data)

    def _calculate_time(self):
        self._delta_time = self._clock.tick(self._framerate) / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self._world, self._delta_time)
        system_movement(self._world, self._delta_time)
        system_bounce(self._world, self._window_w, self._window_h)

    def _draw(self):
        self._screen.fill(self._bg_color)
        system_render(self._world, self._screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
