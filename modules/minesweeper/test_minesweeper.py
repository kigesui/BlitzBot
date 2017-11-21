#!/usr/bin/env python

import unittest

from modules.minesweeper.minesweeper_logic import Board


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
        self.assertEqual(board._game_won(), False)
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
        self.assertEqual(board._game_won(), True)
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
        self.assertEqual(board._game_won(), True)
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
        self.assertEqual(board._game_won(), False)
        return

    def test_lose1(self):
        board = Board()
        board.init(7, 4, 1, 0)
        self.assertEqual(board._game_lose(), False)
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
        self.assertEqual(board._game_lose(), False)
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
        self.assertEqual(board._game_lose(), True)
        return

    def test_reveal(self):
        return

    def test_flag(self):
        return


if __name__ == '__main__':
    unittest.main()
