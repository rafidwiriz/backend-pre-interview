# This is the main code. Run this instead (python main.py)
# Import section
from sudoku import Sudoku

# Main code
# Load all 50 grids from sudoku.txt
grids = []
try:
    f = open("sudoku.txt")
    row = 0
    grid = []
    for line in f:
        if (line.find("Grid") == -1):
            grid.append(list(int(i) for i in line.rstrip("\n")))
            row -= 1
            if (row == 0):
                board = Sudoku(grid)
                grids.append(board)
                grid = []
        else:
            row = 9
finally:
    f.close()

# Solve all sudoku grids
all_sum = 0
for i, grid in enumerate(grids):
    grid.initiate_cell_grid()
    grid.reduce_possibilities()
    if grid.is_any_blank():
        grid.solve()
    print("Grid {}".format(i+1))
    print(grid)
    print("Sum of three top-left cell: {}\n".format(grid.get_sum()))
    all_sum += grid.get_sum()

print("All sum: {}".format(all_sum))