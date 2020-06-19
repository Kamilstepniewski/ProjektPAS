import pygame
import os

pygame.init()

letterX = pygame.image.load(os.path.join('kolko.png'))
letterO = pygame.image.load(os.path.join('Krzyzyk.png'))

font = pygame.font.SysFont("monospace", 30)
label = font.render("New Game", 1, (0,0,0))


class Grid:
    def __init__(self):
        self.grid_lines = [((15,200), (585,200)), # first horizontal line
                           ((15,400), (585,400)), # second horizontal line
                           ((200,15), (200,585)), # first vertical line
                           ((400,15), (400,585))] # second vertical line

        self.grid = [[0 for x in range(3)] for y in range(3)]
        # search directions  N         NW        W       SW       S       SE      E       NE
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False

    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)

        font = pygame.font.SysFont("monospace", 30)
        label = font.render("New Game", 1, (0, 0, 0))
        pygame.draw.rect(surface, (255,255,255), (200, 600, 200, 100))
        surface.blit(label, (225,620))

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(letterX, (x * 200, y * 200))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(letterO, (x * 200, y * 200))

    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def print_grid(self):
        for row in self.grid:
            print(row)

    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0:
            self.set_cell_value(x, y, player)
            self.check_grid(x, y, player)
