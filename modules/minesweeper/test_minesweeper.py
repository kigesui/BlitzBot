#!/usr/bin/env python

import unittest

from modules.minesweeper.minesweeper_logic import Board
from modules.minesweeper.minesweeper_logic import Mine


class TestMinesweeperCommands(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        return


class TestMinesweeperLogic(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_convert(self):
        #  | A  B  C  D  E  F  G
        # 1| 0  1  2  3  4  5  6
        # 2| 7  8  9 10 11 12 13
        # 3|14 15 16 17 18 19 20
        # 4|21 22 23 24 25 26 27
        board = Board()
        board.width = 7
        self.assertNotEqual(board._i2x(0) , 0)
        self.assertEqual(board._i2x(0) , 1)
        self.assertEqual(board._i2x(7) , 1)
        self.assertEqual(board._i2x(2) , 3)
        self.assertEqual(board._i2x(9) , 3)
        self.assertEqual(board._i2x(16), 3)
        self.assertEqual(board._i2x(23), 3)
        self.assertEqual(board._i2x(6) , 7)
        self.assertEqual(board._i2x(13), 7)

        self.assertNotEqual(board._i2y(0) , 0)
        self.assertEqual(board._i2y(0) , 1)
        self.assertEqual(board._i2y(6) , 1)
        self.assertEqual(board._i2y(16), 3)
        self.assertEqual(board._i2y(27), 4)

        self.assertNotEqual(board._xy2i(0, 0), 0)
        self.assertEqual(board._xy2i(1, 1), 0)
        self.assertEqual(board._xy2i(5, 2), 11)
        self.assertEqual(board._xy2i(2, 3), 15)
        self.assertEqual(board._xy2i(7, 4), 27)

    def test_win1(self):
        board = Board()
        board.init(7, 4, 1, 0)
        # shouldnt win: nothing revealed
        self.assertEqual(board.game_won(), False)
        return

    def test_win2(self):
        #  | A  B  C  D  E  F  G |
        # 1| 0  1  x  1  0  0  0 |
        # 2| 0  1  1  1  0  0  0 |
        # 3| 0  0  0  0  0  0  0 |
        # 4| 0  0  0  0  0  0  0 |
        board = Board()
        board.init(7, 4, 1, 0)
        board.cells = [board.REVEALED[0]] * 28
        board.mines[0].x = 3
        board.mines[0].y = 1

        board.cells[2] = board.UNREVEALED
        board.cells[1] = board.REVEALED[1]
        board.cells[3] = board.REVEALED[1]
        board.cells[8] = board.REVEALED[1]
        board.cells[9] = board.REVEALED[1]
        board.cells[10] = board.REVEALED[1]

        # print("printing.........")
        # print(str(board))

        # should win: blank is mine
        self.assertEqual(board.game_won(), True)
        return

    def test_win3(self):
        #  | A  B  C  D  E  F  G |
        # 1| 0  1  x  1  0  0  0 |
        # 2| 0  1  1  1  0  0  0 |
        # 3| 0  0  0  0  0  1  1 |
        # 4| 0  0  0  0  0  1  F |
        board = Board()
        board.init(7, 4, 2, 0)
        board.cells = [board.REVEALED[0]] * 28
        board.mines[0].x = 3
        board.mines[0].y = 1

        board.mines[1].x = 7
        board.mines[1].y = 4

        board.cells[2] = board.UNREVEALED
        board.cells[1] = board.REVEALED[1]
        board.cells[3] = board.REVEALED[1]
        board.cells[8] = board.REVEALED[1]
        board.cells[9] = board.REVEALED[1]
        board.cells[10] = board.REVEALED[1]

        board.cells[27] = board.FLAG
        board.cells[19] = board.REVEALED[1]
        board.cells[20] = board.REVEALED[1]
        board.cells[26] = board.REVEALED[1]

        # print("\n"+str(board))

        # game is won: flagged or blank are mines
        self.assertEqual(board.game_won(), True)
        return

    def test_win4(self):
        #  | A  B  C  D  E  F  G |
        # 1|    1  x  1          |
        # 2|    1  1  1          |
        # 3|                     |
        # 4|                     |
        board = Board()
        board.init(7, 4, 1, 0)
        board.cells = [board.UNREVEALED] * 28
        board.mines[0].x = 3
        board.mines[0].y = 1

        board.cells[2] = board.UNREVEALED
        board.cells[1] = board.REVEALED[1]
        board.cells[3] = board.REVEALED[1]
        board.cells[8] = board.REVEALED[1]
        board.cells[9] = board.REVEALED[1]
        board.cells[10] = board.REVEALED[1]

        # print("printing.........")
        # print(str(board))

        # shouldnt win: not all revealed
        self.assertEqual(board.game_won(), False)
        return

    def test_lose1(self):
        board = Board()
        board.init(7, 4, 1, 0)
        self.assertEqual(board.game_lose(), False)
        return

    def test_lose2(self):
        #  | A  B  C  D  E  F  G |
        # 1|    1  x  1          |
        # 2|    1  1  1          |
        # 3|                     |
        # 4|                     |

        board = Board()
        board.init(7, 4, 1, 0)
        board.cells = [board.UNREVEALED] * 28
        board.mines[0].x = 3
        board.mines[0].y = 1
        board.cells[2] = board.UNREVEALED
        board.cells[1] = board.REVEALED[1]
        board.cells[3] = board.REVEALED[1]
        board.cells[8] = board.REVEALED[1]
        board.cells[9] = board.REVEALED[1]
        board.cells[10] = board.REVEALED[1]
        # no mines are revealed
        self.assertEqual(board.game_lose(), False)
        return

    def test_lose3(self):
        #  | A  B  C  D  E  F  G |
        # 1|    1  *  1          |
        # 2|    1  1  1          |
        # 3|                     |
        # 4|                     |

        board = Board()
        board.init(7, 4, 1, 0)
        board.cells = [board.UNREVEALED] * 28
        board.mines[0].x = 3
        board.mines[0].y = 1

        board.cells[2] = board.MINE
        board.cells[1] = board.REVEALED[1]
        board.cells[3] = board.REVEALED[1]
        board.cells[8] = board.REVEALED[1]
        board.cells[9] = board.REVEALED[1]
        board.cells[10] = board.REVEALED[1]
        # one mine is revealed
        self.assertEqual(board.game_lose(), True)
        return

    def test_reveal1(self):
        #  | A  B  C  D  E  F  G |
        # 1|    R  *  R          |
        # 2|    R  R  R          |
        # 3|                     |
        # 4|                     |

        board = Board()
        board.init(7, 4, 1, 0)
        board.cells = [board.UNREVEALED] * 28
        board.mines[0].x = 3
        board.mines[0].y = 1

        for i in [1, 3, 8, 9, 10]:
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.reveal(x, y), True)
            self.assertEqual(board.reveal(x, y), False)
            self.assertEqual(board.cells[i], board.REVEALED[1])

        i = 2
        x = board._i2x(i)
        y = board._i2y(i)
        self.assertEqual(board.reveal(x, y), True)
        self.assertEqual(board.reveal(x, y), False)
        self.assertEqual(board.cells[i], board.MINE)
        return

    def test_reveal2(self):
        #  | A  B  C  D  E  F  G |
        # 1|    R  *  *  R       |
        # 2|    R  R  R  R       |
        # 3|                     |
        # 4|                     |

        board = Board()
        board.init(7, 4, 2, 0)
        board.cells = [board.UNREVEALED] * 28
        board.mines[0].x = 3
        board.mines[0].y = 1
        board.mines[1].x = 4
        board.mines[1].y = 1

        for i in [1, 4, 8, 11]:
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.reveal(x, y), True)
            self.assertEqual(board.reveal(x, y), False)
            self.assertEqual(board.cells[i], board.REVEALED[1])

        for i in [9, 10]:
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.reveal(x, y), True)
            self.assertEqual(board.reveal(x, y), False)
            self.assertEqual(board.cells[i], board.REVEALED[2])

        for i in [2, 3]:
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.reveal(x, y), True)
            self.assertEqual(board.reveal(x, y), False)
            self.assertEqual(board.cells[i], board.MINE)
        return

    def test_reveal1234567(self):
        #  | A  B  C  D  E  F  G |
        # 1| *  *  *  *  4  2  1 |
        # 2| *  6  5  *  *  *  2 |
        # 3| *  *  4  *  7  *  3 |
        # 4| 2  2  3  *  4  *  2 |

        #  | A  B  C  D  E  F  G
        # 1| 0  1  2  3  4  5  6
        # 2| 7  8  9 10 11 12 13
        # 3|14 15 16 17 18 19 20
        # 4|21 22 23 24 25 26 27

        board = Board()
        board.init(7, 4, 2, 0)
        board.cells = [board.UNREVEALED] * 28

        mines = set([0, 1, 2, 3, 7, 10, 11, 12,
                    14, 15, 17, 19, 24, 26])

        number_cells = {
            0: set([]),
            1: set([6]),
            2: set([5, 13, 21, 22, 27]),
            3: set([20, 23]),
            4: set([4, 16, 25]),
            5: set([9]),
            6: set([8]),
            7: set([18])
        }

        for i in mines:
            mine = Mine(board._i2x(i), board._i2y(i))
            board.mines.append(mine)

        for number in number_cells.keys():
            for i in number_cells[number]:
                rev = number
                x = board._i2x(i)
                y = board._i2y(i)
                self.assertEqual(board.reveal(x, y), True)
                self.assertEqual(board.reveal(x, y), False)
                self.assertEqual(board.cells[i], board.REVEALED[rev])

        for i in mines:
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.cells[i], board.UNREVEALED)
            self.assertEqual(board.reveal(x, y), True)
            self.assertEqual(board.reveal(x, y), False)
            self.assertEqual(board.cells[i], board.MINE)

        return

    def test_reveal12345678(self):
        #  | A  B  C  D  E  F  G |
        # 1| *  *  *  *  *  *  1 |
        # 2| *  8  *  7  6  5  3 |
        # 3| *  *  *  *  *  *  * |
        # 4| 2  3  3  4  *  4  2 |

        #  | A  B  C  D  E  F  G
        # 1| 0  1  2  3  4  5  6
        # 2| 7  8  9 10 11 12 13
        # 3|14 15 16 17 18 19 20
        # 4|21 22 23 24 25 26 27

        board = Board()
        board.init(7, 4, 2, 0)
        board.cells = [board.UNREVEALED] * 28

        mines = set([0, 1, 2, 3, 4, 5, 7, 9,
                    14, 15, 16, 17, 18, 19, 20, 25])

        number_cells = {
            0: set([]),
            1: set([6]),
            2: set([21, 27]),
            3: set([13, 22, 23]),
            4: set([24, 26]),
            5: set([12]),
            6: set([11]),
            7: set([10]),
            8: set([8])
        }

        for i in mines:
            mine = Mine(board._i2x(i), board._i2y(i))
            board.mines.append(mine)

        for number in number_cells.keys():
            for i in number_cells[number]:
                rev = number
                x = board._i2x(i)
                y = board._i2y(i)
                self.assertEqual(board.reveal(x, y), True)
                self.assertEqual(board.reveal(x, y), False)
                self.assertEqual(board.cells[i], board.REVEALED[rev])

        for i in mines:
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.cells[i], board.UNREVEALED)
            self.assertEqual(board.reveal(x, y), True)
            self.assertEqual(board.reveal(x, y), False)
            self.assertEqual(board.cells[i], board.MINE)

        return

    def test_reveal012(self):
        #  | A  B  C  D  E  F  G |
        # 1| 0  0  0  0  0  0  0 |
        # 2| 0  1  2  2  1  0  0 |
        # 3| 0  1  *  *  1  0  0 |
        # 4| 0  1        1  0  0 |

        #  | A  B  C  D  E  F  G
        # 1| 0  1  2  3  4  5  6
        # 2| 7  8  9 10 11 12 13
        # 3|14 15 16 17 18 19 20
        # 4|21 22 23 24 25 26 27

        board = Board()
        board.init(7, 4, 2, 0)
        board.cells = [board.UNREVEALED] * 28

        mines = set([16, 17])

        number_cells = {
            0: set([0, 1, 2, 3, 4, 5, 6,
                   7, 12, 13, 14, 19, 20,
                   21, 26, 27]),
            1: set([8, 15, 22, 11, 18, 25]),
            2: set([9, 10])
        }

        for i in mines:
            mine = Mine(board._i2x(i), board._i2y(i))
            board.mines.append(mine)

        i = 0
        x = board._i2x(i)
        y = board._i2y(i)
        self.assertEqual(board.reveal(x, y), True)
        self.assertEqual(board.reveal(x, y), False)

        for number in number_cells.keys():
            for i in number_cells[number]:
                rev = number
                self.assertEqual(board.cells[i], board.REVEALED[rev])

        for i in mines:
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.cells[i], board.UNREVEALED)
            self.assertEqual(board.reveal(x, y), True)
            self.assertEqual(board.reveal(x, y), False)
            self.assertEqual(board.cells[i], board.MINE)

    def test_flag1(self):
        #  | A  B  C  D  E  F  G |
        # 1|    1  F  F  1       |
        # 2|    1  2  2  1       |
        # 3|                     |
        # 4|                     |

        board = Board()
        board.init(7, 4, 2, 0)
        board.cells = [board.UNREVEALED] * 28

        mines = set([2, 3])

        number_cells = {
            0: set([0, 5, 6,
                   7, 12, 13,
                   14, 15, 16, 17, 18, 19, 20,
                   21, 22, 23, 24, 25, 26, 27]),
            1: set([1, 4, 8, 11]),
            2: set([9, 10]),
            3: set([]),
            4: set([]),
            5: set([]),
            6: set([]),
            7: set([]),
            8: set([])
        }

        for i in mines:
            mine = Mine(board._i2x(i), board._i2y(i))
            board.mines.append(mine)

        # toggle flagging on mines
        for i in mines:
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.cells[i], board.UNREVEALED)
            self.assertEqual(board.flag(x, y), True)
            self.assertEqual(board.cells[i], board.FLAG)
            self.assertEqual(board.flag(x, y), True)
            self.assertEqual(board.cells[i], board.UNREVEALED)

        # toggle flagging on numbers
        for number in number_cells.keys():
            for i in number_cells[number]:
                rev = number
                x = board._i2x(i)
                y = board._i2y(i)
                self.assertEqual(board.cells[i], board.UNREVEALED)
                self.assertEqual(board.flag(x, y), True)
                self.assertEqual(board.cells[i], board.FLAG)
                self.assertEqual(board.flag(x, y), True)
                self.assertEqual(board.cells[i], board.UNREVEALED)
                board.cells[i] = board.REVEALED[rev]
                self.assertEqual(board.flag(x, y), False)

        return

    def test_reveal_flag(self):
        board = Board()
        board.init(7, 4, 2, 0)
        board.cells = [board.FLAG] * 28
        for i in range(28):
            x = board._i2x(i)
            y = board._i2y(i)
            self.assertEqual(board.reveal(x, y), False)

    def test_reveal_flag_boundaries(self):
        board = Board()
        board.init(7, 4, 2, 0)
        board.cells = [board.UNREVEALED] * 28
        self.assertEqual(board.reveal(0, 1), False)
        self.assertEqual(board.reveal(8, 1), False)
        self.assertEqual(board.reveal(1, 0), False)
        self.assertEqual(board.reveal(1, 5), False)
        self.assertEqual(board.flag(0, 1), False)
        self.assertEqual(board.flag(8, 1), False)
        self.assertEqual(board.flag(1, 0), False)
        self.assertEqual(board.flag(1, 5), False)



    # def test_system1(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
