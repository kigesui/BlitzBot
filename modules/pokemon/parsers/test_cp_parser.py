from . import CpParser, CpStrParser, ParserException
import unittest

from data import IV

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
        pokemons, _ = CpParser().parse_args(argline)
        self.assertEqual(pokemons, [])

    def testParseFailExpectException(self):
        argline = "--wtf"
        with self.assertRaisesRegex(ParserException,
                                    "^usage:.*$"):
            CpParser().parse_args(argline)

    def testParseHelp(self):
        argline = "--help"
        usage_regex = "^usage:((.|\n)*)?positional arguments:.*?"
        with self.assertRaisesRegex(ParserException, usage_regex):
            CpParser().parse_args(argline)

    def testParseSimple(self):
        argline = "pidgey"
        pokemons, _ = CpParser().parse_args(argline)
        self.assertEqual(len(pokemons), 1)
        self.assertEqual(16 in pokemons, True)

    def testParseTwo(self):
        argline = "pidgey rattata"
        pokemons, _ = CpParser().parse_args(argline)
        self.assertEqual(len(pokemons), 2)
        self.assertTrue(16 in pokemons)
        self.assertTrue(19 in pokemons)

    def testParseSame(self):
        argline = "pidgey rattata pidgey"
        pokemons, _ = CpParser().parse_args(argline)
        self.assertEqual(len(pokemons), 2)
        self.assertTrue(16 in pokemons)
        self.assertTrue(19 in pokemons)

    def testParseWithDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-l list1"
        pokemons, _ = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokemons), 2)
        self.assertTrue(16 in pokemons)
        self.assertTrue(19 in pokemons)

    def testParseWithTwoDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata'],
            'list2': ['pikachu', 'raticate']
        }
        argline = "-l \"list1 list2\""
        pokemons, _ = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokemons), 4)
        self.assertTrue(16 in pokemons)
        self.assertTrue(19 in pokemons)
        self.assertTrue(25 in pokemons)
        self.assertTrue(20 in pokemons)

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
        argline = '-l list1 pidgey "mr. mime" sandshrew'
        pokemons, _ = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokemons), 4)
        self.assertTrue(16 in pokemons)
        self.assertTrue(19 in pokemons)
        self.assertTrue(122 in pokemons)
        self.assertTrue(27 in pokemons)

    #def testParseIncorrect(self):
    #    argline = "asd qwe"
    #    with self.assertRaisesRegex(ParserException,
    #                                ".*?is not a pokemon.*?"):
    #        CpParser().parse_args(argline)

    def testParseFuzzyWuzzy(self):
        argline = "pigey rattat"
        pokemons, _ = CpParser().parse_args(argline)
        self.assertEqual(len(pokemons), 2)
        self.assertTrue(16 in pokemons)
        self.assertTrue(19 in pokemons)


class TestCpStrArgparse(unittest.TestCase):

    def setUp(self):
        # clear singleton
        CpStrParser.instance = None
        pass

    def tearDown(self):
        pass

    def testParseBreakCorrect(self):
        argline = "-b 5"
        _, _, break_len = CpStrParser().parse_args(argline)
        self.assertEqual(break_len, 5)

    def testParseBreakInvalidExpectException(self):
        argline = "-b -5"
        with self.assertRaisesRegex(ParserException, ".*?"):
            CpStrParser().parse_args(argline)

        argline = "-b a"
        with self.assertRaisesRegex(ParserException,
                                    ".*?usage:*?"):
            CpStrParser().parse_args(argline)

    def testParseSpecificIV(self):
        argline = "-iv fff"
        _, iv_set, break_len = CpStrParser().parse_args(argline)
        self.assertEqual(len(iv_set), 1)
        self.assertTrue(IV(attack=15, defense=15, stamina=15) in iv_set)

        argline = '-iv "fff abc"'
        _, iv_set, break_len = CpStrParser().parse_args(argline)
        self.assertEqual(len(iv_set), 2)
        self.assertTrue(IV(attack=15, defense=15, stamina=15) in iv_set)
        self.assertTrue(IV(attack=0xa, defense=0xb, stamina=0xc) in iv_set)
