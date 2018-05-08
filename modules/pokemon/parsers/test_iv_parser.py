from . import IVParser, ParserException

from data import IV
import unittest


class TestIVParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testParseString1ExpectCorrect(self):
        iv_str = "000"
        results = IVParser().parse_str(iv_str)
        self.assertEqual(len(results), 1)
        self.assertTrue(IV(0, 0, 0) in results)

        iv_str = "fff"
        results = IVParser().parse_str(iv_str)
        self.assertEqual(len(results), 1)
        self.assertTrue(IV(0xf, 0xf, 0xf) in results)

        iv_str = "abc"
        results = IVParser().parse_str(iv_str)
        self.assertEqual(len(results), 1)
        self.assertTrue(IV(0xa, 0xb, 0xc) in results)

    def testParseStringsInvalidExpectException(self):
        iv_str = "hat"
        with self.assertRaises(ParserException):
            IVParser().parse_str(iv_str)

        iv_str = "hat cat"
        with self.assertRaises(ParserException):
            IVParser().parse_str(iv_str)

        iv_str = "-55"
        with self.assertRaises(ParserException):
            IVParser().parse_str(iv_str)

    def testParseMultiStringsExpectCorrect(self):
        iv_str = "000 001 002"
        results = IVParser().parse_str(iv_str)
        self.assertEqual(len(results), 3)
        self.assertTrue(IV(0, 0, 0) in results)
        self.assertTrue(IV(0, 0, 1) in results)
        self.assertTrue(IV(0, 0, 2) in results)

        ivs = []
        for x in range(0, 0xfff+1):
            ivs.append('%03x' % x)
        iv_str = ' '.join(ivs)
        results = IVParser().parse_str(iv_str)
        self.assertEqual(len(results), 16**3)
        for a in range(0, 0xf+1):
            for d in range(0, 0xf+1):
                for s in range(0, 0xf+1):
                    self.assertTrue(IV(a, d, s) in results)
