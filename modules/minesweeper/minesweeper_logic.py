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

    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = []  # list of chars
        self.mines = []  # list of Mines
        return

    # conversion functions
    def _i2x(self, i):
        return i % self.width + 1

    def _i2y(self, i):
        return int(i / self.width) + 1

    def _xy2i(self, x, y):
        return (y-1)*self.width+(x-1)

    # print
    def __str__(self):
        num_flag = self.cells.count(self.FLAG)
        board_str = "Mines Remaining:{}\n".format(len(self.mines)-num_flag)
        board_str += "__|"
        # print col header
        for i in range(self.width):
            board_str += "{:_>2}".format(chr(0x40+i+1))

        # print each row
        for y in range(self.height):
            y += 1
            board_str += "\n{:>2}|".format(y)
            for x in range(self.width):
                x += 1
                i = self._xy2i(x, y)
                board_str += "{:>2}".format(self.cells[i])

        return board_str

    # init
    def init(self, w, h, num_mines, seed=0):
        self.width = w
        self.height = h
        num_cells = self.height * self.width
        self.cells = [self.UNREVEALED] * num_cells
        self.mines = []

        # place mines
        if seed != 0:
            rand.seed(seed)
        possible_spaces = set(range(num_cells))
        mines_places = rand.sample(possible_spaces, num_mines)
        for i in mines_places:
            x = self._i2x(i)
            y = self._i2y(i)
            self.mines.append(Mine(x, y))
        return

    # game won
    def game_won(self):
        # if num_reveal + num_mines == total
        total = len(self.cells)
        num_reveal = 0
        for c in self.cells:
            if c in self.REVEALED:
                num_reveal += 1
        return num_reveal + len(self.mines) == total

    # game lose
    def game_lose(self):
        # if a mine is revealed
        for m in self.mines:
            i = self._xy2i(m.x, m.y)
            if self.cells[i] == self.MINE:
                return True
        return False

    # checks if x and y are valid
    def check_xy(func):
        def func_warpper(self, x, y):
            if x < 1 or x > self.width:
                return False
            if y < 1 or y > self.height:
                return False
            return func(self, x, y)
        return func_warpper

    # flag
    # returns false if number or mine
    @check_xy
    def flag(self, x, y):
        i = self._xy2i(x, y)
        if self.cells[i] == self.UNREVEALED:
            self.cells[i] = self.FLAG
            return True
        if self.cells[i] == self.FLAG:
            self.cells[i] = self.UNREVEALED
            return True
        return False

    # reveal
    # returns false if already revealed or invalid
    @check_xy
    def reveal(self, x, y):
        i = self._xy2i(x, y)
        if self.cells[i] == self.UNREVEALED:
            num_mines = 0
            for m in self.mines:
                if m.x == x and m.y == y:
                    # set mine
                    self.cells[i] = self.MINE
                    return True
                if abs(m.x-x) <= 1 and abs(m.y-y) <= 1:
                    num_mines += 1
            # set number
            self.cells[i] = self.REVEALED[num_mines]
            if num_mines == 0:
                self.reveal(x-1, y-1)
                self.reveal(x-1, y )
                self.reveal(x-1, y+1)
                self.reveal(x, y-1)
                self.reveal(x, y+1)
                self.reveal(x+1, y-1)
                self.reveal(x+1, y )
                self.reveal(x+1, y+1)
            return True
        return False
