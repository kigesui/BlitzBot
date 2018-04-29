from . import CpParser, CpStrParser, ParserException
import unittest

# import sys
# from os import path
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# sys.path.append(path.dirname(path.abspath(__file__)))


class TestCpArgparse(unittest.TestCase):

    def setUp(self):
        # clear singleton
        CpParser.instance = None
        pass

    def tearDown(self):
        pass

    def testParseEmpty(self):
        argline = ""
        pokes = CpParser().parse_args(argline)
        self.assertEqual(pokes, [])

    def testParseFailExpectException(self):
        argline = "--halp"
        with self.assertRaisesRegex(ParserException,
                                    "^usage:.*$"):
            CpParser().parse_args(argline)

    def testParseSimple(self):
        argline = "pidgey"
        pokes = CpParser().parse_args(argline)
        self.assertEqual(len(pokes), 1)
        self.assertEqual(16 in pokes, True)

    def testParseTwo(self):
        argline = "pidgey rattata"
        pokes = CpParser().parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertTrue(16 in pokes)
        self.assertTrue(19 in pokes)

    def testParseSame(self):
        argline = "pidgey rattata pidgey"
        pokes = CpParser().parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertTrue(16 in pokes)
        self.assertTrue(19 in pokes)

    def testParseWithDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-l list1"
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertTrue(16 in pokes)
        self.assertTrue(19 in pokes)

    def testParseWithTwoDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata'],
            'list2': ['pikachu', 'raticate']
        }
        argline = "-l \"list1 list2\""
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 4)
        self.assertTrue(16 in pokes)
        self.assertTrue(19 in pokes)
        self.assertTrue(25 in pokes)
        self.assertTrue(20 in pokes)

    def testParseWithWrongDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-l \"list1 list2 list3\" pidgey"
        with self.assertRaisesRegex(ParserException,
                                    "list2 is not a valid list"):
            CpParser(pokedict).parse_args(argline)

    def testParseDoubleQuote(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-l list1 pidgey \"mr. mime\" sandshrew"
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 4)
        self.assertTrue(16 in pokes)
        self.assertTrue(19 in pokes)
        self.assertTrue(122 in pokes)
        self.assertTrue(27 in pokes)

    def testParseIncorrect(self):
        argline = "asd qwe"
        with self.assertRaisesRegex(ParserException,
                                    ".*?is not a pokemon.*?"):
            CpParser().parse_args(argline)

    # todo:
    # def testParseFuzzyWuzzy(self):
    #     argline = "pigey rattat"
    #     pokes = CpParser().parse_args(argline)
    #     self.assertEqual(len(pokes), 2)
    #     self.assertEqual(16 in pokes, True)
    #     self.assertEqual(19 in pokes, True)


class TestCpStrArgparse(unittest.TestCase):

    def setUp(self):
        # clear singleton
        CpStrParser.instance = None
        pass

    def tearDown(self):
        pass

    def testParseBreakCorrect(self):
        argline = "-b 5"
        _, break_len = CpStrParser().parse_args(argline)
        self.assertEqual(break_len, 5)

    def testParseBreakNegative(self):
        argline = "-b -5"
        with self.assertRaisesRegex(ParserException, ".*?"):
            CpStrParser().parse_args(argline)

    def testParseBreakIncorrect(self):
        argline = "-b a"
        with self.assertRaisesRegex(ParserException,
                                    ".*?usage:*?"):
            CpStrParser().parse_args(argline)
