"""An idle-animated character controlled with A and D."""

from pathlib import Path
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, load_image
from emote import Emote


class Player:
    FRAME_SIZE = 64
    DRAW_SIZE = FRAME_SIZE * 2
    COLUMNS = 8
    ROWS = 2
    FRAME_COUNT = COLUMNS * ROWS
    ANIMATION_FPS = 10
    MOVE_SPEED = 240  # pixels per second

    def __init__(self, x, ground_y, screen_width):
        image_path = (Path(__file__).resolve().parent.parent
                      / "image" / "character" / "idle" / "idle_blue.png")
        self.image = load_image(str(image_path))
        self.x = x
        self.y = ground_y + self.DRAW_SIZE / 2
        self.screen_width = screen_width
        self.facing = 1
        self.animation_time = 0.0
        self.pressed_keys = set()
        self.emote = Emote()

    def handle_event(self, event):
        self.emote.handle_event(event)
        if event.type == SDL_KEYDOWN and event.key in (SDLK_a, SDLK_d):
            self.pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP and event.key in (SDLK_a, SDLK_d):
            self.pressed_keys.discard(event.key)

    def update(self, dt):
        self.emote.update(dt)
        direction = int(SDLK_d in self.pressed_keys) - int(SDLK_a in self.pressed_keys)
        if direction:
            self.facing = direction
        self.x += direction * self.MOVE_SPEED * dt
        half_size = self.DRAW_SIZE / 2
        self.x = max(half_size, min(self.screen_width - half_size, self.x))
        self.animation_time = (self.animation_time + dt) % (
            self.FRAME_COUNT / self.ANIMATION_FPS
        )

    def draw(self):
        frame = int(self.animation_time * self.ANIMATION_FPS) % self.FRAME_COUNT
        left = (frame % self.COLUMNS) * self.FRAME_SIZE
        # pico2d clips from the bottom; play the top row first.
        bottom = (self.ROWS - 1 - frame // self.COLUMNS) * self.FRAME_SIZE
        self.image.clip_composite_draw(
            left, bottom, self.FRAME_SIZE, self.FRAME_SIZE,
            # The original sprite faces left, so flip it when moving right.
            0, "h" if self.facing > 0 else "",
            self.x, self.y, self.DRAW_SIZE, self.DRAW_SIZE,
        )
        self.emote.draw(self.x, self.y + self.DRAW_SIZE / 2)
