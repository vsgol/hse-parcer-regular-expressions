import sys
import unittest
import parser as pr


class TestChar(unittest.TestCase):
    def test_Char(self):
        a = pr.Char('a')

        self.assertFalse(a(""))
        self.assertFalse(a("b"))
        self.assertFalse(a("aa"))
        self.assertTrue(a("a"))

        a = pr.Char('\n')

        self.assertFalse(a(""))
        self.assertFalse(a("b"))
        self.assertFalse(a("aa"))
        self.assertTrue(a("\n"))


class TestStar(unittest.TestCase):
    def test_Char(self):
        aaa = pr.Star(pr.Char('a'))

        self.assertTrue(aaa(""))
        self.assertTrue(aaa("aaaaaa"))
        self.assertTrue(aaa("a" * 4500))
        self.assertFalse(aaa("b"))

    def test_Alt(self):
        ab = pr.Star(pr.Alt(pr.Char('a'), pr.Char('b')))
        self.assertTrue(ab("aaaaa" * 1000))
        self.assertFalse(ab("cbabcabcbaaaccbabcabbac"))
        self.assertTrue(ab("babaaa" * 1000))
        self.assertFalse(ab("babaaa" * 1000 + 'c'))

        abc = pr.Star(pr.Alt(pr.Char('a'), pr.Char('b'), pr.Char('c'), pr.Char('a')))
        self.assertTrue(abc("aabbcb"))
        self.assertTrue(abc("cbabcabcbaaaccbabcabbac"))
        self.assertTrue(abc("cbab" * 1000))
        self.assertFalse(abc("aasbbcb"))

    def test_Seq(self):
        abb = pr.Star(pr.Seq(pr.Char('a'), pr.Char('b'), pr.Char('b')))
        self.assertTrue(abb(""))
        self.assertTrue(abb("abb"))
        self.assertTrue(abb("abbabb"))
        self.assertTrue(abb("abb" * 3000))
        self.assertFalse(abb("ab"))
        self.assertFalse(abb("aab"))
        self.assertFalse(abb("abbabba"))

        aabac = pr.Star(pr.Seq(pr.Char('a'), pr.Char('a'), pr.Char('b'), pr.Char('a'), pr.Char('c')))
        self.assertTrue(aabac("aabacaabac"))
        self.assertFalse(aabac("aabbc"))
        self.assertTrue(aabac("aabac" * 1500))
        self.assertFalse(aabac("aasbbcb"))


class TestSeq(unittest.TestCase):
    def test_Seq(self):
        aaa = pr.Seq(pr.Char('a'), pr.Char('a'), pr.Char('a'))

        self.assertTrue(aaa("aaa"))
        self.assertFalse(aaa("aa"))
        self.assertFalse(aaa("aaaa"))
        self.assertFalse(aaa("aab"))
        self.assertFalse(aaa(""))

        aaaa = pr.Seq(*[pr.Char(i) for i in "a"*300])

        self.assertFalse(aaaa("aa"))
        self.assertFalse(aaaa("aaaa"))
        self.assertFalse(aaaa("aab"))
        self.assertFalse(aaaa(""))
        self.assertTrue(aaaa("a"*300))

    def test_Alt(self):
        ab = pr.Seq(pr.Alt(pr.Char('a'), pr.Char('b')), pr.Char('a'))

        self.assertTrue(ab("ba"))
        self.assertTrue(ab("aa"))
        self.assertFalse(ab("a"))
        self.assertFalse(ab("b"))
        self.assertFalse(ab("bb"))
        self.assertFalse(ab("baa"))


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

        self.assertTrue(digit("1"))
        self.assertFalse(digit("a"))

        self.assertTrue(number("1"))
        self.assertTrue(number("+1"))
        self.assertTrue(number("-1"))
        self.assertTrue(number("+0"))
        self.assertTrue(number("-1121241291281683"))
        self.assertFalse(number("a"))
        self.assertFalse(number("-"))
        self.assertFalse(number("-01"))

        self.assertTrue(float_("17523.1423123e-12127653"))
        self.assertFalse(float_("17523.1423123e-12-2"))
        self.assertTrue(float_("1" * 3000 + "." + "1e+" + "1" * 3000))


class TestSpeedSlow(unittest.TestCase):
    def test_Complicated(self):
        aaa = pr.Alt(pr.Seq(pr.Char('a'),
                            pr.Seq(pr.Char('a'),
                                   pr.Star(pr.Char('a')))),
                     pr.Star(pr.Char('aa')),
                     pr.Char('a'),
                     pr.Seq(pr.Star(pr.Char('a')),
                            pr.Seq(pr.Char('a'),
                                   pr.Star(pr.Char('a')))))
        self.assertTrue(aaa("a" * 800))


class TestSpeedFast(unittest.TestCase):
    def test_Easy(self):
        a = pr.Star(pr.Char('a'))
        self.assertTrue(a("a" * 800))


class TestFor2Seconds(unittest.TestCase):
    def test(self):
        a = pr.Star(pr.Char('a'))
        self.assertTrue(a("a" * 1000000))


if __name__ == '__main__':
    sys.setrecursionlimit(4000)
    unittest.main()
