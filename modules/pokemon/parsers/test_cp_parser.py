from . import CpParser, ParserException
import unittest


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
        self.assertEqual("pidgey" in pokes, True)

    def testCpParseTwo(self):
        argline = "pidgey rattata"
        pokes = CpParser().parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertEqual("pidgey" in pokes, True)
        self.assertEqual("rattata" in pokes, True)

    def testCpParseSame(self):
        argline = "pidgey rattata pidgey"
        pokes = CpParser().parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertEqual("pidgey" in pokes, True)
        self.assertEqual("rattata" in pokes, True)

    def testCpParseWithDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-a list1"
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 2)
        self.assertEqual("pidgey" in pokes, True)
        self.assertEqual("rattata" in pokes, True)

    def testCpParseWithTwoDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata'],
            'list2': ['pikachu', 'raticate']
        }
        argline = "-a \"list1 list2\""
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 4)
        self.assertEqual("pidgey" in pokes, True)
        self.assertEqual("rattata" in pokes, True)
        self.assertEqual("rattata" in pokes, True)
        self.assertEqual("raticate" in pokes, True)

    def testCpParseWithWrongDict(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "-a \"list1 list2 list3\" pidgey"
        with self.assertRaisesRegex(ParserException,
                                    "list2 is not a valid list"):
            CpParser(pokedict).parse_args(argline)

    def testCpParseDoubleQuote(self):
        pokedict = {
            'list1': ['pidgey', 'rattata']
        }
        argline = "--a list1 pidgey \"mr. meme\" sandshrew"
        pokes = CpParser(pokedict).parse_args(argline)
        self.assertEqual(len(pokes), 4)
        self.assertEqual("pidgey" in pokes, True)
        self.assertEqual("rattata" in pokes, True)
        self.assertEqual("mr. meme" in pokes, True)
        self.assertEqual("sandshrew" in pokes, True)

    # todo
    # def testCpParseIncorrect(self):
    #     argline = "pigey rattat"
    #     pokes = CpParser().parse_args(argline)
    #     self.assertEqual(len(pokes), 2)
    #     self.assertEqual("pidgey" in pokes, True)
    #     self.assertEqual("rattata" in pokes, True)
