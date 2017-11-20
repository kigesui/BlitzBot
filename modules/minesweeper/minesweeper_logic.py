import random as rand


class Mine:
    x = -1
    y = -1

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Board:

    UNREVEALED = ' '
    REVEALED = "012345678"
    FLAG = 'F'
    MINE = '*'

    width = 0
    height = 0
    cells = []  # list of chars
    mines = []  # list of Mines

    def __init__(self):
        return

    # conversion functions
    def _i2x(self, i):
        return i % self.width + 1

    def _i2y(self, i):
        return i / self.width + 1

    def _xy2i(self, x, y):
        return (y-1)*self.width+(x-1)

    # print
    def __str__(self):
        board_str = "   |"
        # print col header
        for i in range(self.width):
            board_str += "{:>3}".format(chr(0x40+i+1))

        # print each row
        for y in range(self.height):
            y += 1
            board_str += "\n{:>3}|".format(y)
            for x in range(self.width):
                x += 1
                i = self._xy2i(x, y)
                board_str += "{:>3}".format(self.cells[i])

        return board_str

    # init
    def init(self, w, h, num_mines, seed=0):
        self.width = w
        self.height = h
        self.num_mines = num_mines
        num_cells = self.height * self.width
        self.cells = [self.UNREVEALED] * num_cells

        if seed != 0:
            rand.seed(seed)

        # place mines
        possible_spaces = set(range(num_cells))
        mines_places = rand.sample(possible_spaces, self.num_mines)

        for i in mines_places:
            x = self._i2x(i)
            y = self._i2y(i)
            self.mines.append(Mine(x, y))

        return
