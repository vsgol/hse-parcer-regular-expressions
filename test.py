import sys
import unittest
import parser as pr


class TestStar(unittest.TestCase):
    def test_Char(self):
        aaa = pr.Star(pr.Char('a'))
        self.assertTrue(aaa(""))
        self.assertTrue(aaa("aaaaaa"))
        self.assertTrue(aaa("a" * 450))
        self.assertFalse(aaa("b"))

    def test_Alt(self):
        abc = pr.Star(pr.Alt(pr.Char('a'), pr.Char('b'), pr.Char('c'), pr.Char('a')))
        self.assertTrue(abc("aabbcb"))
        self.assertTrue(abc("cbabcabcbaaaccbabcabbac"))
        self.assertTrue(abc("cbab" * 100))
        self.assertFalse(abc("aasbbcb"))

    def test_Seq(self):
        aabac = pr.Star(pr.Seq(pr.Char('a'), pr.Char('a'), pr.Char('b'), pr.Char('a'), pr.Char('c')))
        self.assertTrue(aabac("aabacaabac"))
        self.assertFalse(aabac("aabbc"))
        self.assertTrue(aabac("aabac" * 90))
        self.assertFalse(aabac("aasbbcb"))


class TestEps(unittest.TestCase):
    def test_Eps(self):
        eps = pr.Eps()
        self.assertTrue(eps(""))
        self.assertFalse(eps("a" * 12000))


class TestAll(unittest.TestCase):
    def test_Float(self):
        pos_digit = pr.Alt(*[pr.Char(i) for i in "123456789"])
        digit = pr.Alt(*[pr.Char(i) for i in "1234567890"])

        number = pr.Seq(pr.Alt(pr.Eps(), pr.Alt(pr.Char('+'), pr.Char("-"))),
                        pr.Alt(pr.Char('0'), pr.Seq(pos_digit, pr.Star(digit))))

        float_ = pr.Alt(pr.Seq(pr.Alt(number,
                                      pr.Eps()),
                               pr.Char("."),
                               pr.Star(digit),
                               pr.Alt(pr.Seq(pr.Char("e"),
                                             number),
                                      pr.Eps())),
                        pr.Seq(number,
                               pr.Char("."),
                               pr.Alt(pr.Seq(pr.Star(digit),
                                             pr.Alt(pr.Seq(pr.Char("e"),
                                                           number),
                                                    pr.Eps())),
                                      pr.Eps())))

        self.assertTrue(float_("17523.1423123e-12127653"))
        self.assertFalse(float_("17523.1423123e-12-2"))
        self.assertTrue(float_("1" * 300 + "." + "1e+" + "1" * 300))


class TestSpeedSlow(unittest.TestCase):
    def test_Complicated(self):
        aaa = pr.Alt(pr.Seq(pr.Char('a'), pr.Seq(pr.Char('a'), pr.Star(pr.Char('a')))), pr.Star(pr.Char('a')),
                     pr.Star(pr.Char('a')))
        self.assertTrue(aaa("a" * 800))


class TestSpeedFast(unittest.TestCase):
    def test_Easy(self):
        a = pr.Star(pr.Char('a'))
        self.assertTrue(a("a" * 750))


if __name__ == '__main__':
    sys.setrecursionlimit(4000)
    unittest.main()
