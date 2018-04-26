from . import CpParser, ParserException
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

    def testCpParseEmpty(self):
        argline = ""
        pokes = CpParser().parse_args(argline)
        self.assertEqual(pokes, [])

    def testCpParseFailExpectException(self):
        argline = "--halp"
        with self.assertRaisesRegex(ParserException,
                                    "^usage:.*$"):
            CpParser().parse_args(argline)

    def testCpParseSimple(self):
        argline = "pidgey"
        pokes = CpParser().parse_args(argline)
        self.assertEqual(len(pokes), 1)
        self.assertEqual(16 in pokes, True)

    def testCpParseTwo(self):
        argline = "pidgey rattata"
        pokes = CpParser().parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertEqual(16 in pokes, True)
        self.assertEqual(19 in pokes, True)

    def testCpParseSame(self):
        argline = "pidgey rattata pidgey"
        pokes = CpParser().parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertEqual(16 in pokes, True)
        self.assertEqual(19 in pokes, True)

    def testCpParseWithDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-l list1"
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertEqual(16 in pokes, True)
        self.assertEqual(19 in pokes, True)

    def testCpParseWithTwoDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata'],
            'list2': ['pikachu', 'raticate']
        }
        argline = "-l \"list1 list2\""
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 4)
        self.assertEqual(16 in pokes, True)
        self.assertEqual(19 in pokes, True)
        self.assertEqual(25 in pokes, True)
        self.assertEqual(20 in pokes, True)

    def testCpParseWithWrongDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-l \"list1 list2 list3\" pidgey"
        with self.assertRaisesRegex(ParserException,
                                    "list2 is not a valid list"):
            CpParser(pokedict).parse_args(argline)

    def testCpParseDoubleQuote(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-l list1 pidgey \"mr. mime\" sandshrew"
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 4)
        self.assertEqual(16 in pokes, True)
        self.assertEqual(19 in pokes, True)
        self.assertEqual(122 in pokes, True)
        self.assertEqual(27 in pokes, True)

    def testCpParseIncorrect(self):
        argline = "asd qwe"
        with self.assertRaisesRegex(ParserException,
                                    ".*?is not a pokemon.*?"):
            CpParser().parse_args(argline)

    # todo:
    # def testCpParseFuzzyWuzzy(self):
    #     argline = "pigey rattat"
    #     pokes = CpParser().parse_args(argline)
    #     self.assertEqual(len(pokes), 2)
    #     self.assertEqual(16 in pokes, True)
    #     self.assertEqual(19 in pokes, True)
