import pygame as pg
from GridCell import *
from class_definitions import *

window_size = pg.Vector2(450, 700)
board_loc = pg.Vector2(1, 90)
board_size = pg.Vector2(window_size.x-2, window_size.x)
cell_size = window_size.x//9
grid = []

for r in range(9):
    grid.append([])
    for c in range(9):
        grid[r].append(GridCell(r, c))


pg.init()

screen = pg.display.set_mode([window_size.x, window_size.y])

running = True
while running:

    # Did the user click the window close button?
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    drawCells(screen, grid, cell_size, board_loc)

    drawBorders(screen, cell_size, board_loc, board_size)

    # Flip the display
    pg.display.flip()

# Done! Time to quit.
pg.quit()