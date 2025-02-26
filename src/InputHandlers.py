import pygame


class KeyHandler:

    def __init__(self):
        self.inputs = {}

    def get_inputs(self):
        return self.inputs

    def get_key(self, key):
        input_ = False
        keys = pygame.key.get_pressed()

        if keys[key] and not self.inputs[key]:
            input_ = True
            self.inputs[key] = True

        if not keys[key]:
            self.inputs[key] = False

        return input_


class ClickHandler:
    def __init__(self):
        self.inputs = {0: (-1, -1), 1: (-1, -1)}
        self.tile_size = 30

    def get_inputs(self):
        return self.inputs

    def set_tile_size(self, tile_size):
        self.tile_size = tile_size

    def handle_click(self):
        clicks = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        grid_pos = (pos[0] // self.tile_size, pos[1] // self.tile_size)

        if grid_pos != self.inputs[1]:
            self.inputs[1] = grid_pos

        if clicks[0]:
            return 1, grid_pos, pos

        elif clicks[2]:
            return 0, grid_pos, pos
