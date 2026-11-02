"""Layered forest background. Run: python code/background.py"""

from pathlib import Path
from time import perf_counter
from ctypes import byref

from pico2d import (
    SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE,
    clear_canvas, close_canvas, delay, get_events, load_image,
    open_canvas, update_canvas,
    SDL_DisplayMode, SDL_GetDesktopDisplayMode, SDL_Init, SDL_INIT_VIDEO,
)
from player import Player

IMAGE_DIR = Path(__file__).resolve().parent.parent / "image"
WINDOW_WIDTH = 928
WINDOW_HEIGHT = 793
GROUND_Y = 52  # Walking surface, measured from the bottom of the artwork.


class Background:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        self.width = width
        self.height = height
        # Sky (0011) to nearest ground (0000), including both Lights layers.
        paths = sorted((IMAGE_DIR / "background").glob("Layer_*.png"), reverse=True)
        if not paths:
            raise FileNotFoundError(f"No background layers in {IMAGE_DIR / 'background'}")
        self.layers = [load_image(str(path)) for path in paths]

    def draw(self):
        for layer in self.layers:
            layer.draw(self.width / 2, self.height / 2, self.width, self.height)


def main():
    # Use the monitor's native resolution rather than stretching a small window.
    SDL_Init(SDL_INIT_VIDEO)
    display_mode = SDL_DisplayMode()
    if SDL_GetDesktopDisplayMode(0, byref(display_mode)) != 0:
        raise RuntimeError("Cannot determine the desktop display resolution")
    width, height = display_mode.w, display_mode.h
    open_canvas(width, height, full=True)
    try:
        background = Background(width, height)
        ground_y = GROUND_Y * height / WINDOW_HEIGHT
        player = Player(width / 2, ground_y, width)
        running = True
        previous_time = perf_counter()
        while running:
            current_time = perf_counter()
            dt = min(current_time - previous_time, 0.05)
            previous_time = current_time
            for event in get_events():
                if event.type == SDL_QUIT or (
                    event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                ):
                    running = False
                player.handle_event(event)
            if not running:
                break
            player.update(dt)
            clear_canvas()
            background.draw()
            player.draw()
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
