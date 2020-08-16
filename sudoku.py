import math
from cell import Cell

class Sudoku:
    def __init__(self, grid):
        self.grid = grid # 2d list of sudoku numbers
        self.cell_grid = [] # 1d list of Cell objects
        self.box_length = int(math.sqrt(len(self.grid))) # Length of sudoku box
        self.blank_cells = {} # dictionary of cells that are blank

    def __str__(self):
        # Formatted Sudoku object into 2d-board-like string
        # Return type: string
        strings_grid = []
        for row_idx in range(len(self.grid)):
            if row_idx % self.box_length == 0:
                strings_grid.append('-'.join(['-'] * (self.box_length ** 2)))
            row = self.grid[row_idx]
            strings_row = []
            i = 0
            while i < len(row):
                strings_row.append(' '.join(str(n) for n in row[i:i+self.box_length]))
                i += self.box_length
            strings_grid.append('|'.join(strings_row))
        return "\n".join(strings_grid[1:])

    def get_sum(self):
        # Get sum of three top-left-to-right cells
        # Return type: int
        return sum(self.grid[0][0:3])

    def get_row(self, x):
        # Get all numbers from row x
        # Return type: list
        return self.grid[x]

    def get_column(self, y):
        # Get all numbers from column y
        # Return type: list
        return [row[y] for row in self.grid]

    def get_box_start(self, coordinate):
        # Get start coordinate of a box
        # Return type: int
        return coordinate - (coordinate % self.box_length)

    def get_box(self, x, y):
        # Get all numbers from box where cell (x, y) is
        # Return type: list
        x0, y0 = self.get_box_start(x), self.get_box_start(y)
        box = []
        for i in range(x0, x0 + self.box_length):
            box.extend(self.grid[i][y0:y0+self.box_length])
        return box

    def set_blank_cells(self):
        # Set all blank cells in grid
        i = 0
        for j, cell in enumerate(self.cell_grid):
            if cell.blank:
                self.blank_cells[i] = j
                i += 1

    def set_cell(self, cell):
        # Set cell number with probability numbers, and update grid of numbers
        # Return type: Cell
        cell.set_number()
        self.update_cell(cell)
        return cell

    def initiate_cell_grid(self):
        # Initiate grid of Cell objects
        for i in range(len(self.grid)):
            self.cell_grid.extend([Cell(i, j, self.grid[i][j]) for j in range(len(self.grid[i]))])

    def reduce_possibilities(self):
        # Reduce probability numbers of each of Cell objects. If there is one probability remain, set the number
        # Repeat process when a one-probability Cell object has been handled
        i = 0
        while i < len(self.cell_grid):
            x, y = self.cell_grid[i].get_coordinate()
            available_num = list(set(self.get_row(x) + self.get_column(y) + self.get_box(x, y)))
            self.cell_grid[i].reduce_possibilities(available_num)
            if self.cell_grid[i].is_one_possibility():
                self.cell_grid[i].handle_one_possibility()
                self.update_cell(self.cell_grid[i])
                i = 0
            else:
                i += 1

    def update_cell(self, cell):
        # Update grid of numbers by cell
        x, y = cell.get_coordinate()
        self.grid[x][y] = cell.get_number()

    def is_any_blank(self):
        # Check if there is any blank Cell objects
        # Return type: bool
        for cell in self.cell_grid:
            if cell.blank:
                return True
        return False

    def check_duplicate(self, area):
        # Check if there is any duplicate in selected area
        # Return type: bool
        numbers = [x for x in area if x != 0]
        return len(numbers) == len(set(numbers))

    def is_valid(self, x, y):
        # Check if a cell (x, y) area is valid (no duplicates)
        # Return type: bool
        for area in [self.get_row(x), self.get_column(y), self.get_box(x, y)]:
            if not self.check_duplicate(area):
                return False
        return True

    def reset_cell(self, cell):
        # Reset Cell objects
        cell.possible_index = 0
        cell.number = 0
        self.update_cell(cell)

    def solve(self):
        # Solve sudoku grid
        self.set_blank_cells()
        i = 0
        while i < len(self.blank_cells):
            cell = self.cell_grid[self.blank_cells[i]]
            cell = self.set_cell(cell)
            x, y = cell.get_coordinate()
            while (not self.is_valid(x, y)) and (cell.possible_index < len(cell.possibilities) - 1):
                cell.possible_index += 1
                cell = self.set_cell(cell)
            if self.is_valid(x, y):
                i += 1
            else:
                while cell.possible_index == len(cell.possibilities) - 1:
                    self.reset_cell(cell)
                    i -= 1
                    cell = self.cell_grid[self.blank_cells[i]]
                cell.possible_index += 1

if __name__ == "__main__":
    # This is driver section for this classes
    # Main code is in main.py file
    grid = [[0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 5, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 2, 0, 3, 0, 0, 9],
            [0, 0, 5, 0, 1, 0, 3, 0, 0]]
    grid2 = [[0, 0, 0, 0, 0, 0, 9, 0, 7],
            [0, 0, 0, 4, 2, 0, 1, 8, 0],
            [0, 0, 0, 7, 0, 5, 0, 2, 6],
            [1, 0, 0, 9, 0, 4, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 5, 0, 7, 0, 0, 9],
            [9, 2, 0, 1, 0, 8, 0, 0, 0],
            [0, 3, 4, 0, 5, 9, 0, 0, 0],
            [5, 0, 7, 0, 0, 0, 0, 0, 0]]
    
    sudoku_grid = Sudoku(grid)
    print(sudoku_grid, "\n")
    sudoku_grid.initiate_cell_grid()
    sudoku_grid.reduce_possibilities()
    if sudoku_grid.is_any_blank():
        sudoku_grid.solve()
    print(sudoku_grid)