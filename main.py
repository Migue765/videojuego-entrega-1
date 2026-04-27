#!/usr/bin/python3
"""Punto de entrada – compatible con pygbag (web) y escritorio."""

import asyncio
import os

# Top-level imports so pygbag's dependency scanner detects them  # noqa: F401
import pygame   # noqa: F401
import esper    # noqa: F401

# Fix working directory for PyInstaller bundles and pygbag web runner
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from src.engine.game_engine import GameEngine

# Create engine at module level so pygbag doesn't hit
# "The video driver did not add any displays" inside the coroutine
engine = GameEngine()


async def main():
    engine._create()
    engine.is_running = True
    while engine.is_running:
        engine._calculate_time()
        engine._process_events()
        engine._update()
        engine._draw()
        await asyncio.sleep(0)   # yield to the browser event loop
    engine._clean()


if __name__ == "__main__":
    asyncio.run(main())
