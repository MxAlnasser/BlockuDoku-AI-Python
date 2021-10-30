import pygame as pg
from GridCell import *
from class_definitions import *
#put shapes in here
shapes = {

}

class Blockudoku:
    __init__(self):
        self.window_size = pg.Vector2(450, 700)
        self.board_loc = pg.Vector2(1, 90)
        self.board_size = pg.Vector2(window_size.x-2, window_size.x)
        self.cell_size = window_size.x//9
        self.grid = []

        for r in range(9):
            self.grid.append([])
            for c in range(9):
                self.grid[r].append(GridCell(r, c))


        self.pg.init()

        self.screen = pg.display.set_mode([window_size.x, window_size.y])

        running = True
        while running:

            # Did the user click the window close button?
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # Fill the background with white
            self.screen.fill((255, 255, 255))

            self.drawCells(screen, grid, cell_size, board_loc)

            self.drawBorders(screen, cell_size, board_loc, board_size)

            # Flip the display
            self.pg.display.flip()

        # Done! Time to quit.
        pg.quit()
    
    def _check_complete_three_by_three(self, cell_number):
        start_col =(cell_number % 2) * 3
        stop_col = (cell_number % 2) + 1) * 3
        start_row = 0
        stop_row = 0
        #first row
        if(cell_number <= 2):
            start_row = 0
            stop_row = 2
        elif(cell_number <= 5):
            start_row = 3
            stop_row = 5
        else(cell_number <= 8):
            start_row = 6
            stop_row = 8
        