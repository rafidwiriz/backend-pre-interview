class Cell:
    def __init__(self, x, y, num):
        self.x_pos = x # cell row position
        self.y_pos = y # cell column position
        self.number = num # cell number
        self.blank = True if num == 0 else False # bool indicate if cell is blank or not
        self.possibilities = list(range(1, 10)) if self.blank else [] # list of possible numbers for this cell, if it's blank
        self.possible_index = 0 # index of current possibilities list

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return str(self.number)

    def get_coordinate(self):
        # Get coordinate of a cell
        # Return type: (int, int)
        return self.x_pos, self.y_pos

    def get_number(self):
        # Get number of cell
        # Return type: int
        return self.number

    def set_number(self):
        # Set number of cell with value from possible_index of possibilities list
        if len(self.possibilities) > 0:
            self.number = self.possibilities[self.possible_index]

    def reduce_possibilities(self, list):
        # Reduce possibilities list elements by input list
        if self.blank:
            self.possibilities = [x for x in self.possibilities if x not in list]

    def is_one_possibility(self):
        # Check if there is only one possible number of a cell
        # Return type: bool
        return len(self.possibilities) == 1

    def handle_one_possibility(self):
        # Handle cell that has only one possible number
        if self.is_one_possibility():
            self.set_number()
            self.blank = False
            self.possibilities = []

if __name__ == "__main__":
    # This is driver section for this classes
    # Main code is in main.py file
    cell = Cell(0, 0, 0)
    print(cell.possibilities)
    print(cell.get_coordinate())