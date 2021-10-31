import pygame as pg
from GridCell import *
from class_definitions import *
import random
#put shapes in here
#The shape is a set of coordinates. 
#I only put this few ones because we want something that works first
shapes = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'Z': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'S': [(0, 0), (-1, -1), (0, -1), (1, 0)],
    'I': [(0, 0), (0, -1), (0, -2), (0, -3)],
    'O': [(0, 0), (0, -1), (-1, 0), (-1, -1)],
    'LJ': [(0, 0), (-1, 0), (-2, 0), (0, -1), (0, -2)],
    'LL': [(0, 0), (1, 0), (2, 0), (0, -1), (0, -2)],
    '.': [(0,0)],
    '..': [(0,0), (0,1)],
    '|': [(0,0), (0,1), (0,2)]
}
shapes_keys = list(shapes.keys())
print(shapes_keys)

def rotated(shape):
    return [(-j, i) for i, j in shape]

class Blockudoku:
    
    def __init__(self, seed):
        random.seed(seed)
        window_size = pg.Vector2(450, 700)
        board_loc = pg.Vector2(1, 90)
        board_size = pg.Vector2(window_size.x-2, window_size.x)
        cell_size = window_size.x//9
        self.grid = []

        for r in range(9):
            self.grid.append([])
            for c in range(9):
                self.grid[r].append(GridCell(r, c))


        pg.init()

        screen = pg.display.set_mode([window_size.x, window_size.y])

        running = True
        while running:

            # Fill the background with white
            screen.fill((255, 255, 255))

            drawCells(screen, self.grid, cell_size, board_loc)

            drawBorders(screen, cell_size, board_loc, board_size)

            #DO TURN LOGIC HERE
            next_shape = self._make_shape(shapes[shapes_keys[random.randint(0,len(shapes_keys)-1)]])
            #find out valid positions
            valid_positions = self._get_valid_locations(next_shape)
            self.grid_to_matrix()

            ###DECISION LOGIC HERE
            # valid_position is a list of ALL valid spots
            # next_shape is the next possible shape 
            # self.matrix is a boolean array of all filled in spots








            #decision needs to be a tuple (row, col)
            decision = (0,0)
            ###DECISION LOGIC HERE
            self._place_shape(next_shape, decision)

            # Did the user click the window close button?
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                

            # Flip the display
            pg.display.flip()

        # Done! Time to quit.
        pg.quit()

    ### grid to matrix
    # This will turn the 2D array of GridCell to a 2D matrix of bools
    def _grid_to_matrix(self):
        self.matrix = []
        for row in self.grid:
            sub_arr = []
            for column in row:
                if column.empty:
                    sub_arr.append(1)
                else:
                    sub_arr.append(0)
            self.matrix.append(sub_arr)


    def _place_shape(self, shape, spot):
        for piece in shape:
            self.grid[spot[0] + piece[0]][spot[1] + piece[1]].empty = False
        

    def _get_valid_locations(self, shape):
        valid_placing_points = []
        for row in range(9):
            for col in range(9):
                if self._check_if_fits(shape, (row,col)):
                    valid_placing_points.append((row,col))
        return valid_placing_points
    
    def _check_if_fits(self, shape, spot):
        #spot is a tuple (row,col)
        fits = True
        row_g = spot[0]
        col_g = spot[1]
        for direction in shape:
            #check if each coordinate in the shape fits
            row_s = direction[0]
            col_s = direction[1]
            if row_g + row_s >= 9:
                return False
            elif col_g + col_s >= 9:
                return False
            elif row_g + row_s <= 0:
                return False
            elif col_g + col_s <= 0:
                return False
            elif not self.grid[row_g+row_s][col_g+col_s].empty:
                return False
        return True

    def _make_shape(self, shape):
        return_shape = shape
        for i in range(random.randint(0,15)):
            return_shape = rotated(return_shape)
        return return_shape

    def _check_complete_three_by_three(self, cell_number):
        start_col =(cell_number % 3) * 3
        stop_col = ((cell_number % 3) + 1) * 3
        start_row = 0
        stop_row = 0
        #first row
        if(cell_number <= 2):
            start_row = 0
            stop_row = 3
        elif(cell_number <= 5):
            start_row = 3
            stop_row = 6
        elif(cell_number <= 8):
            start_row = 6
            stop_row = 9
        
        all_filled = True
        for col in range(start_col,stop_col):
            for row in range(start_row, stop_row):
                if self.grid[row][col].empty:
                    return False
        for col in range(start_col,stop_col):
            for row in range(start_row, stop_row):
                self.grid[row][col].empty = True
        return True
    
    def _check_complete_row(self):
        completed_rows = []
        for row in range(9):
            completed = True
            for col in range(9):
                if self.grid[row][col]:
                    completed = False
            if completed:
                completed_rows.append(row)
        return completed_rows

    def _check_complete_col(self):
        completed_cols = []
        for col in range(9):
            completed = True
            for row in range(9):
                if self.grid[row][col]:
                    completed = False
            if completed:
                completed_cols.append(col)
        return completed_cols
    
    def _check_score(self):
        rows_done = self._check_complete_row()
        cols_done = self._check_complete_col()
        filled_3x3 = []
        for i in range(9):
            if self._check_complete_three_by_three():
                filled_3x3.append(i)
        #Now everything that can get points is in rows_done, cols_done, and filled_3x3
        #20 points per row, col, and 3 by 3
        score = (len(rows_done) + len(cols_done) + len(filled_3x3)) * 20

        #reset column
        for row in rows_done:
            for col in range(9):
                self.grid[row][col].empty = True
        #reset rows
        for col in cols_done:
            for row in range(9):
                self.grid[row][col].empty = True
        return score


game = Blockudoku(69)
game._check_complete_three_by_three(3)
print(game._check_complete_three_by_three(3))