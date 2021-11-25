# TODO: Calculate state

import pygame as pg
from GridCell import *
from ClassDefinitions import *
from Shape import *
import random
import time

MOVEMENT_PUNISHMENT = -1
INVALID_MOVEMENT_PUNISHMENT = -10
INVALID_PLACEMENT_PUNISHMENT = -20
LOSE_PUNISHMENT = 0

# # put shapes in here
# # The shape is a set of coordinates.
# # I only put this few ones because we want something that works first
# shapes = {
#     'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
#     'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
#     'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
#     'Z': [(0, 0), (-1, 0), (0, -1), (1, -1)],
#     'S': [(0, 0), (-1, -1), (0, -1), (1, 0)],
#     'I': [(0, 0), (0, -1), (0, -2), (0, -3)],
#     'O': [(0, 0), (0, -1), (-1, 0), (-1, -1)],
#     'LJ': [(0, 0), (-1, 0), (-2, 0), (0, -1), (0, -2)],
#     'LL': [(0, 0), (1, 0), (2, 0), (0, -1), (0, -2)],
#     '.': [(0, 0)],
#     '..': [(0, 0), (0, 1)],
#     '|': [(0, 0), (0, 1), (0, 2)],
# }
# shapes_keys = list(shapes.keys())
# print(shapes_keys)


def rotated(shape):
    return [(-j, i) for i, j in shape]


class Blockudoku:

    def __init__(self, seed):
        random.seed(seed)
        self.window_size = pg.Vector2(450, 700)
        self.board_loc = pg.Vector2(1, 90)
        self.board_size = pg.Vector2(self.window_size.x - 2, self.window_size.x)
        self.cell_size = self.window_size.x // 9
        self.grid = []
        self.score = 0
        self.cleared_recently = False
        self.lost = False
        self.state = None

        for r in range(9):
            self.grid.append([])
            for c in range(9):
                self.grid[r].append(GridCell(r, c))

        self.current_shape = Shape()

    def message_display(self, screen):
        font = pg.font.SysFont(None, 44)
        if self.lost:
            color = (255, 0, 0)
        else:
            color = (0, 0, 0)
        img = font.render('Score: ' + str(self.score), True, color)
        screen.blit(img, (self.window_size.x/2 - 60, 37))



    def drawGame(self, screen):
        running = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.step(0)
                if event.key == pg.K_RIGHT:
                    self.step(1)
                if event.key == pg.K_DOWN:
                    self.step(2)
                if event.key == pg.K_LEFT:
                    self.step(3)
                if event.key == pg.K_UP:
                    self.step(4)
                self.drawGame(screen)


        screen.fill((255, 255, 255))

        drawCells(screen, self.grid, self.cell_size, self.board_loc)
        self.current_shape.draw(screen, self.board_loc, self.cell_size, self.grid)
        drawBorders(screen, self.cell_size, self.board_loc, self.board_size)
        self.message_display(screen)

        pg.display.flip()


        # #DO TURN LOGIC HERE
        # next_shape = self._make_shape(shapes[shapes_keys[random.randint(0, len(shapes_keys)-1)]])
        # #find out valid positions
        # valid_positions = self._get_valid_locations(next_shape)
        # self._grid_to_matrix()
        #
        # print(next_shape)
        # ###DECISION LOGIC HERE
        # # valid_position is a list of ALL valid spots
        # # next_shape is the next possible shape
        # # self.matrix is a boolean array of all filled in spots
        # print("Valid positions are: ")
        # print(valid_positions)
        #
        # choice = int(input("Where do you want to place the block?"))
        # decision = valid_positions[choice]

        # decision needs to be a tuple (row, col)
        ###DECISION LOGIC HERE
        # self._place_shape(next_shape, decision)
        # print(self._generate_score_array(decision, next_shape))

        # Did the user click the window close button?


        return running

    def step(self, action):
        if action == 0:  # place
            valid = self.current_shape.place(self.grid)
            if valid:
                reward = self._blockPlaced()
                return self.state, reward, self.lost
            else:
                return self.state, INVALID_PLACEMENT_PUNISHMENT, self.lost

        if action == 1:
            valid = self.current_shape.moveRight()
        elif action == 2:
            valid = self.current_shape.moveDown()
        elif action == 3:
            valid = self.current_shape.moveLeft()
        else:
            valid = self.current_shape.moveUp()

        if valid:
            return self.state, MOVEMENT_PUNISHMENT, self.lost
        else:
            return self.state, INVALID_MOVEMENT_PUNISHMENT, self.lost

    def _scoreBoard(self):
        cleared_blocks = []

        # check for vertical lines
        for row in range(9):
            cleared = True
            for col in range(9):
                if self.grid[row][col].empty:
                    cleared = False
                    break

            if cleared:
                cleared_blocks += self.grid[row]

        # check for horizontal lines
        for col in range(9):
            cleared = True
            for row in range(9):
                if self.grid[row][col].empty:
                    cleared = False
                    break

            if cleared:
                cleared_blocks += [grid_row[col] for grid_row in self.grid]

        # check for cleared squares
        for square_row in range(0, 9, 3):
            for square_col in range(0, 9, 3):
                cleared = True
                for row in range(3):
                    for col in range(3):
                        if self.grid[square_row+row][square_col+col].empty:
                            cleared = False
                            break

                if cleared:

                    for row in range(3):
                        for col in range(3):
                            cleared_blocks.append(self.grid[square_row+row][square_col+col])

        # give score
        reward = 0
        if len(cleared_blocks) > 0:
            if len(cleared_blocks) <= 18:
                reward += len(cleared_blocks) * 2
            else:
                reward += len(cleared_blocks) * 4

            for cleared_block in cleared_blocks:
                cleared_block.empty = True

        return reward

    def _blockPlaced(self):
        reward = 0
        reward += self._scoreBoard()
        if reward > 0:
            if self.cleared_recently:
                reward += 9
            self.cleared_recently = True
        else:
            self.cleared_recently = False

        reward += self.current_shape.remainingBlocks(self.grid)
        self.score += reward

        self.current_shape = Shape()
        if not self.current_shape.validSpaceExists(self.grid):
            self.lost = True
            reward -= LOSE_PUNISHMENT

        return reward







    # def _check_four_directions(self, point, matrix):
    #     edges = 0
    #     row = point[0]
    #     col = point[1]
    #     if not self.grid[row][col].empty:
    #         # this is a block
    #         return 5
    #     if row - 1 < 0 or matrix[row - 1][col]:
    #         edges += 1
    #     if row + 1 > 8 or matrix[row + 1][col]:
    #         edges += 1
    #     if col - 1 < 0 or matrix[row][col - 1]:
    #         edges += 1
    #     if col + 1 > 8 or matrix[row][col + 1]:
    #         edges += 1
    #
    #     return edges
    #
    # def _generate_score_array(self, choice, shape):
    #     # Array is 4 values returned
    #     # 0 block border
    #     # 1 block border
    #     # 2 block border
    #     # 3 block border
    #     # 4 block border
    #     matrix = self._grid_to_matrix()
    #     # place block in that matrix
    #     for location in shape:
    #         matrix[choice[0] + location[0]][choice[1] + location[1]] = 1
    #     array = [0, 0, 0, 0, 0, 0]
    #     # this matrix is easier to traverse
    #     for row in range(9):
    #         for col in range(9):
    #             array[self._check_four_directions((row, col), matrix)] += 1
    #     return array
    #
    # def _get_next_states(self, shape, grid):
    #     next_valid_pos = self._get_valid_locations(shape)
    #     states = {}
    #     for choice in next_valid_pos:
    #         states[choice] = self._generate_score_array(choice, shape)
    #     return states
    #
    # ### grid to matrix
    # # This will turn the 2D array of GridCell to a 2D matrix of bools
    # def _grid_to_matrix(self):
    #     self.matrix = []
    #     for row in self.grid:
    #         sub_arr = []
    #         for column in row:
    #             if not column.empty:
    #                 sub_arr.append(1)
    #             else:
    #                 sub_arr.append(0)
    #         self.matrix.append(sub_arr)
    #     return self.matrix
    #
    # def _place_shape(self, shape, spot):
    #     for piece in shape:
    #         self.grid[spot[0] + piece[0]][spot[1] + piece[1]].empty = False
    #
    # def _get_valid_locations(self, shape):
    #     valid_placing_points = []
    #     for row in range(9):
    #         for col in range(9):
    #             if self._check_if_fits(shape, (row, col)):
    #                 valid_placing_points.append((row, col))
    #     return valid_placing_points
    #
    # def _make_shape(self, shape):
    #     return_shape = shape
    #     for i in range(random.randint(0, 15)):
    #         return_shape = rotated(return_shape)
    #     return return_shape
    #
    # def _check_complete_three_by_three(self, cell_number):
    #     start_col = (cell_number % 3) * 3
    #     stop_col = ((cell_number % 3) + 1) * 3
    #     start_row = 0
    #     stop_row = 0
    #     # first row
    #     if (cell_number <= 2):
    #         start_row = 0
    #         stop_row = 3
    #     elif (cell_number <= 5):
    #         start_row = 3
    #         stop_row = 6
    #     elif (cell_number <= 8):
    #         start_row = 6
    #         stop_row = 9
    #
    #     all_filled = True
    #     for col in range(start_col, stop_col):
    #         for row in range(start_row, stop_row):
    #             if self.grid[row][col].empty:
    #                 return False
    #     for col in range(start_col, stop_col):
    #         for row in range(start_row, stop_row):
    #             self.grid[row][col].empty = True
    #     return True
    #
    # def _check_complete_row(self):
    #     completed_rows = []
    #     for row in range(9):
    #         completed = True
    #         for col in range(9):
    #             if self.grid[row][col]:
    #                 completed = False
    #         if completed:
    #             completed_rows.append(row)
    #     return completed_rows
    #
    # def _check_complete_col(self):
    #     completed_cols = []
    #     for col in range(9):
    #         completed = True
    #         for row in range(9):
    #             if self.grid[row][col]:
    #                 completed = False
    #         if completed:
    #             completed_cols.append(col)
    #     return completed_cols
    #
    # def _check_score(self):
    #     rows_done = self._check_complete_row()
    #     cols_done = self._check_complete_col()
    #     filled_3x3 = []
    #     for i in range(9):
    #         if self._check_complete_three_by_three():
    #             filled_3x3.append(i)
    #     # Now everything that can get points is in rows_done, cols_done, and filled_3x3
    #     # 20 points per row, col, and 3 by 3
    #     score = (len(rows_done) + len(cols_done) + len(filled_3x3)) * 20
    #
    #     # reset column
    #     for row in rows_done:
    #         for col in range(9):
    #             self.grid[row][col].empty = True
    #     # reset rows
    #     for col in cols_done:
    #         for row in range(9):
    #             self.grid[row][col].empty = True
    #     return score


game = Blockudoku(69)


pg.init()

screen = pg.display.set_mode([game.window_size.x, game.window_size.y])

running = True
while running:
    running = game.drawGame(screen)

pg.quit()
