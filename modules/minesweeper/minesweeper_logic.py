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
        board_str += "_|"

        # print each row
        for y in range(self.height):
            y += 1
            board_str += "\n{:>2}|".format(y)
            for x in range(self.width):
                x += 1
                i = self._xy2i(x, y)
                board_str += "{:>2}".format(self.cells[i])
            board_str += " |"
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
        num_mines = len(self.mines)
        for c in self.cells:
            if c in self.REVEALED:
                num_reveal += 1
        cond1 = num_reveal > 0
        cond2 = num_reveal == (total - num_mines)
        return cond1 and cond2

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
            for m in self.mines:
                if m.x == x and m.y == y:
                    # set mine
                    self.cells[i] = self.MINE
                    return True
            # set number
            num_mines = self._count_mines(x, y)
            self.cells[i] = self.REVEALED[num_mines]
            if num_mines == 0:
                self.expand(x, y)
            return True
        return False

    # reveal
    # returns false if cannot expand
    @check_xy
    def expand(self, x, y):
        i = self._xy2i(x, y)
        if self.cells[i] in self.REVEALED:
            expect_num_flags = self.REVEALED.index(self.cells[i])
            actual_num_flags = self._count_flags(x, y)

            if expect_num_flags == actual_num_flags:
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

    def _count_mines(self, x, y):
        num_mines = 0
        for m in self.mines:
            if abs(m.x-x) <= 1 and abs(m.y-y) <= 1:
                num_mines += 1
        return num_mines

    def _count_flags(self, x, y):
        num_flags = 0
        scan_cells = [(x-1, y-1), (x, y-1), (x+1, y-1),
                      (x-1, y), (x+1, y),
                      (x-1, y+1), (x, y+1), (x+1, y+1)]
        for fx, fy in scan_cells:
            if fx < 0 or fx > self.width:
                continue
            if fy < 0 or fy > self.height:
                continue
            i = self._xy2i(fx, fy)
            if self.cells[i] == self.FLAG:
                num_flags += 1
        return num_flags
