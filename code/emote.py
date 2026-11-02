"""Three-frame emotes shown above the player with the 1 and 2 keys."""

from pathlib import Path

from pico2d import SDL_KEYDOWN, SDLK_1, SDLK_2, load_image


class Emote:
    FRAME_SIZE = 16
    DRAW_SIZE = 48
    ROW_FROM_TOP = 9
    FRAME_COUNT = 3
    ANIMATION_FPS = 6
    DURATION = 1.0
    GAP = 8
    FIRST_COLUMNS = {SDLK_1: 0, SDLK_2: 3}

    def __init__(self):
        image_path = (Path(__file__).resolve().parent.parent
                      / "image" / "emote" / "emote.png")
        self.image = load_image(str(image_path))
        self.first_column = None
        self.elapsed = 0.0

    def handle_event(self, event):
        if (event.type == SDL_KEYDOWN
                and event.key in self.FIRST_COLUMNS
                and not getattr(event, "repeat", False)):
            self.first_column = self.FIRST_COLUMNS[event.key]
            self.elapsed = 0.0

    def update(self, dt):
        if self.first_column is not None:
            self.elapsed += dt
            if self.elapsed >= self.DURATION:
                self.first_column = None

    def draw(self, x, player_top):
        if self.first_column is None:
            return
        frame = int(self.elapsed * self.ANIMATION_FPS) % self.FRAME_COUNT
        left = (self.first_column + frame) * self.FRAME_SIZE
        # Sheet rows count from the top; pico2d clips from the bottom.
        bottom = self.image.h - self.ROW_FROM_TOP * self.FRAME_SIZE
        self.image.clip_draw(
            left, bottom, self.FRAME_SIZE, self.FRAME_SIZE,
            x, player_top + self.GAP + self.DRAW_SIZE / 2,
            self.DRAW_SIZE, self.DRAW_SIZE,
        )
