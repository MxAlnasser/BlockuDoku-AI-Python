import pygame as pg

class loc:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def drawCells(screen, grid, cell_size, board_loc):
    for r in range(9):
        for c in range(9):
            grid[r][c].draw(screen, board_loc, cell_size)


def drawBorders(screen, cell_size, board_loc, board_size):
    color = (0, 0, 0)

    rect = pg.Rect(board_loc.x + cell_size*3, board_loc.y, cell_size*3, board_size.y)
    pg.draw.rect(screen, color, rect, 2)
    rect = pg.Rect(board_loc.x, board_loc.y + cell_size*3, board_size.x, cell_size*3)
    pg.draw.rect(screen, color, rect, 2)

    rect = pg.Rect(board_loc.x, board_loc.y, board_size.x, board_size.y)
    pg.draw.rect(screen, color, rect, 3)
