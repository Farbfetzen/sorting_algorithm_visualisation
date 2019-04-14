import os
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg
import sorting_algorithms


ALGORITHMS = {"Bubble sort": sorting_algorithms.BubbleSort}
BACKGROUND_COLOR = (255, 255, 255)
RECT_COLOR = (50, 50, 50)
COMPARISON_COLOR = (0, 100, 200)
ALL_SORTED_COLOR = (0, 128, 0)
TEXT_COLOR = (110, 0, 110)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
N_VALUES = 100
COLUMN_WIDTH = 8
COLUMN_HEIGHT_MULTIPLIER = 5
UPS = 300  # updates per second
UPDATE_DELAY = 1 / UPS  # time between updates in seconds
START_PAUSED = True
TEXT_PADDING = 2
FONT_SIZE = 18


class Main:
    def __init__(self, algorithm_name):
        values = list(range(1, N_VALUES + 1))
        random.shuffle(values)
        self.algorithm = ALGORITHMS[algorithm_name](values)
        self.main_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("sorting algorithm visualisation")
        self.running = True
        self.update_timer = 0
        self.paused = START_PAUSED
        self.restart = False
        # self.font = pg.font.Font(None, FONT_SIZE)
        self.font = pg.font.SysFont("sans", FONT_SIZE)
        self.name_text = self.font.render(algorithm_name, True, TEXT_COLOR)
        self.comparisons_text = self.font.render("comparisons: ", True, TEXT_COLOR)
        self.swaps_text = self.font.render("swaps: ", True, TEXT_COLOR)
        self.comparisons_text_width = self.comparisons_text.get_rect().width
        self.swaps_text_width = self.swaps_text.get_rect().width
        self.text_height = self.name_text.get_rect().height

    def handle_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pg.K_RETURN:
                    self.algorithm.update()
                elif event.key == pg.K_r:
                    self.restart = True
                    self.running = False
                elif event.key == pg.K_d:
                    print(self.update_timer)

    def draw(self):
        self.main_surface.fill(BACKGROUND_COLOR)
        for i, v in enumerate(self.algorithm.values):
            if self.algorithm.is_sorted:
                color = ALL_SORTED_COLOR
            elif i in self.algorithm.comparisons:
                color = COMPARISON_COLOR
            else:
                color = RECT_COLOR
            pg.draw.rect(
                self.main_surface,
                color,
                (
                    i * COLUMN_WIDTH,
                    WINDOW_HEIGHT - v * COLUMN_HEIGHT_MULTIPLIER,
                    COLUMN_WIDTH,
                    v * COLUMN_HEIGHT_MULTIPLIER
                )
            )
        comparison_count_text = self.font.render(
            str(self.algorithm.comparison_count), True, TEXT_COLOR
        )
        swap_count_text = self.font.render(
            str(self.algorithm.swaps_count), True, TEXT_COLOR
        )
        self.main_surface.blit(self.name_text, (TEXT_PADDING, TEXT_PADDING))
        self.main_surface.blit(
            self.comparisons_text,
            (TEXT_PADDING, TEXT_PADDING + self.text_height)
        )
        self.main_surface.blit(
            self.swaps_text,
            (TEXT_PADDING, TEXT_PADDING * 2 + self.text_height * 2)
        )
        self.main_surface.blit(
            comparison_count_text,
            (
                TEXT_PADDING + self.comparisons_text_width,
                TEXT_PADDING + self.text_height
            )
        )
        self.main_surface.blit(
            swap_count_text,
            (
                TEXT_PADDING + self.swaps_text_width,
                TEXT_PADDING * 2 + self.text_height * 2
            )
        )

    def run(self):
        clock = pg.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000  # in seconds
            if not self.paused:
                self.update_timer += dt
            self.handle_input()
            while self.update_timer >= UPDATE_DELAY:
                self.update_timer -= UPDATE_DELAY
                self.algorithm.update()
            self.draw()
            pg.display.update()
        return self.restart


if __name__ == "__main__":
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.init()
    restart = True
    while restart:
        restart = Main("Bubble sort").run()
