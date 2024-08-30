from math import floor

import pygame as pg
from src.InputHandlers import KeyHandler, ClickHandler


class Game:
    def __init__(self):
        self.show_hud = True
        self.frame_counter = 0
        self.click_handler = ClickHandler
        self.key_handler = KeyHandler
        self.input = {}
        self.last_click_tile_state = None
        self.last_click_pos = None
        self.fps_cap = 120
        self.game_speed = 15
        self.gen = 0
        self.screen = None
        self.clock = None
        self.res = (1920, 1080)
        self.tile_size = 10
        self.grid_res_x = 192
        self.grid_res_y = 108
        self.BG_COLOR = (27, 27, 27)
        self.OBJECTS_COLOR = (255, 255, 255)

        self.running = False
        self.progress = False
        self.grid = []
        self.rect_grid = []
        self.show_grid = False

    def window_init(self):
        pg.init()
        self.screen = pg.display.set_mode(self.res, pg.FULLSCREEN)
        pg.display.set_caption("Game of Life")
        self.clock = pg.time.Clock()

    def grid_init(self):
        grid = []
        for y in range(self.grid_res_y):
            grid.append([0 for _ in range(self.grid_res_x)])
        self.grid = grid

    def draw_grid(self):
        new_rect_grid = []

        for grid_y in range(self.grid_res_y):
            new_rect_grid_row = []
            for grid_x in range(self.grid_res_x):
                screen_y = grid_y * self.tile_size
                screen_x = grid_x * self.tile_size

                rect = pg.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
                new_rect_grid_row.append(rect)

                cell_state = self.grid[grid_y][grid_x]
                color = self.OBJECTS_COLOR if cell_state == 1 else self.BG_COLOR

                pg.draw.rect(self.screen, color, rect)

                if self.show_grid:

                    line = pg.Rect(screen_x, screen_y, self.tile_size, 1)
                    column = pg.Rect(screen_x, screen_y, 1, self.tile_size)
                    pg.draw.rect(self.screen, self.OBJECTS_COLOR, line, 1)
                    pg.draw.rect(self.screen, self.OBJECTS_COLOR, column, 1)
                new_rect_grid_row.append(new_rect_grid_row)

            self.rect_grid = new_rect_grid

    def draw_hud(self):

        font = pg.font.Font("freesansbold.ttf", 32)
        gen_label = font.render(f"Gen {self.gen}", True, self.OBJECTS_COLOR, self.BG_COLOR)
        gen_label_rect = gen_label.get_rect()
        gen_label_rect.bottomright = (self.res[0] - 10, self.res[1] - 10)
        self.screen.blit(gen_label, gen_label_rect)

        speed_label = font.render(f"Speed {floor((self.game_speed/60)*100)}%", True, self.OBJECTS_COLOR, self.BG_COLOR)
        speed_label_rect = speed_label.get_rect()
        speed_label_rect.bottomleft = (10, self.res[1] - 10)
        self.screen.blit(speed_label, speed_label_rect)

    def get_live_neighbors(self, x, y):
        alive_neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    alive_neighbors += self.grid[((y + i) % self.grid_res_y)][((x + j) % self.grid_res_x)]
        return alive_neighbors

    def update(self):

        if self.key_handler.get_key(pg.K_r):
            self.progress = False
            self.grid_init()
            self.gen = 0

        if self.key_handler.get_key(pg.K_h):
            self.show_hud = not self.show_hud

        if self.key_handler.get_key(pg.K_s):
            self.OBJECTS_COLOR, self.BG_COLOR = self.BG_COLOR, self.OBJECTS_COLOR

        if self.key_handler.get_key(pg.K_g):
            self.show_grid = not self.show_grid

        if self.key_handler.get_key(pg.K_SPACE):
            self.progress = not self.progress

        if self.game_speed > 1:
            if self.key_handler.get_key(pg.K_LEFT):
                self.game_speed -= 1

        if self.game_speed < 60:
            if self.key_handler.get_key(pg.K_RIGHT):

                if self.key_handler.get_key(pg.K_LCTRL):
                    self.game_speed = (10 + self.game_speed) if self.game_speed < 51 else 60

                self.game_speed += 1

        if not self.progress:
            click = self.click_handler.handle_click(self.rect_grid)

            if click is not None:
                self.grid[click[1][1]][click[1][0]] = click[0]

        elif self.frame_counter % (self.fps_cap // self.game_speed) == 0:
            new_grid = []

            for y in range(self.grid_res_y):
                new_row = []

                for x in range(self.grid_res_x):
                    alive_neighbors = self.get_live_neighbors(x, y)

                    if self.grid[y][x] == 0:
                        if alive_neighbors == 3:
                            new_row.append(1)
                        else:
                            new_row.append(0)

                    else:
                        if alive_neighbors in [2, 3]:
                            new_row.append(1)
                        else:
                            new_row.append(0)

                new_grid.append(new_row)

            self.grid = new_grid
            self.gen += 1

        self.draw_grid()

        if self.show_hud:
            self.draw_hud()

    def run(self):
        self.running = True

        self.window_init()
        self.grid_init()
        self.key_handler = KeyHandler()
        self.click_handler = ClickHandler()
        self.click_handler.set_tile_size(self.tile_size)

        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.clock.tick(self.fps_cap)

            self.update()

            pg.display.flip()
            self.frame_counter += 1
            if self.frame_counter >= self.fps_cap:
                self.frame_counter = 0
