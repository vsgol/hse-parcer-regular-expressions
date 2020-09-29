def nullable(c):
    if isinstance(c, EmptyC) or isinstance(c, CharC):
        return False
    if isinstance(c, EpsC) or isinstance(c, StarC):
        return True
    if isinstance(c, AltC):
        return nullable(c.first) or nullable(c.second)
    if isinstance(c, SeqC):
        return nullable(c.first) and nullable(c.second)
    raise Exception("Input Error")


class Derives(object):
    def __call__(self, w):
        f = self
        for c in w:
            f = f.derivative(c)
            if isinstance(f, EmptyC):
                return False
        return nullable(f)

    def derivative(self, c, o=None):
        if o is None:
            o = self

        if isinstance(o, EmptyC):
            return EmptyC()

        if isinstance(o, EpsC):
            return EmptyC()

        if isinstance(o, CharC):
            if o.first == c:
                return EpsC()
            return EmptyC()

        if isinstance(o, StarC):
            return Seq(o.first.derivative(c), o)

        if isinstance(o, AltC):
            return Alt(o.first.derivative(c), o.second.derivative(c))

        if isinstance(o, SeqC):
            left_derivative = Seq(o.first.derivative(c), o.second)
            if nullable(o.first):
                return Alt(left_derivative, o.second.derivative(c))
            return left_derivative


class EmptyC(Derives):
    def __init__(self, *args): pass

    def __eq__(self, other):
        if not isinstance(other, EmptyC):
            return False
        return True

    def __str__(self): return "Empty"


class EpsC(Derives):
    def __init__(self, *args): pass

    def __eq__(self, other):
        if not isinstance(other, EpsC):
            return False
        return True

    def __str__(self): return "Eps"


class CharC(Derives):
    def __init__(self, c):
        self.first = c

    def __eq__(self, other):
        if not isinstance(other, CharC):
            return False
        return self.first == other.first

    def __str__(self): return "'{}'".format(self.first)


class SeqC(Derives):
    def __init__(self, f, s, *args):
        if len(args) > 0:
            self.first = f
            self.second = Seq(s, args[0], *args[1:])
        else:
            self.first = f
            self.second = s

    def __eq__(self, other):
        if not isinstance(other, SeqC):
            return False
        return (self.first == other.first) & (self.second == other.second)

    def __str__(self):
        return "(Seq {} {})".format(self.first, self.second)


class AltC(Derives):
    def __init__(self, f, s, *args):
        if len(args) > 0:
            self.first = f
            self.second = Alt(s, args[0], *args[1:])
        else:
            self.first = f
            self.second = s

    def __eq__(self, other):
        if not isinstance(other, AltC):
            return False
        return (self.first == other.first) & (self.second == other.second)

    def __str__(self):
        return "(Alt {} {})".format(self.first, self.second)


class StarC(Derives):
    def __init__(self, f):
        self.first = f

    def __eq__(self, other):
        if not isinstance(other, StarC):
            return False
        return self.first == other.first

    def __str__(self):
        return "(Star {})".format(self.first)


def Eps(*args):
    return EpsC()


def Empty(*args):
    return EmptyC()


def Char(c):
    return CharC(c)


def Seq(f, s, *args):
    if isinstance(f, EmptyC) or isinstance(s, EmptyC):
        return EmptyC()
    if isinstance(f, EpsC):
        return Seq(s, args[0], *args[1:]) if len(args) else s
    if isinstance(s, EpsC):
        return Seq(f, args[0], *args[1:]) if len(args) else f
    if isinstance(f, StarC) and f == s:
        return f
    return SeqC(f, s, *args)


def Alt(f, s, *args):
    if isinstance(f, EmptyC):
        return Alt(s, args[0], *args[1:]) if len(args) else s
    if isinstance(s, EmptyC):
        return Alt(f, args[0], *args[1:]) if len(args) else f
    if isinstance(f, EpsC) and nullable(s):
        return Alt(s, args[0], *args[1:]) if len(args) else s
    if isinstance(s, EpsC) and nullable(f):
        return Alt(f, args[0], *args[1:]) if len(args) else f
    if f == s:
        return Alt(f, args[0], *args[1:]) if len(args) else f
    return AltC(f, s, *args)


def Star(f):
    if isinstance(f, StarC):
        return f
    if isinstance(f, (EpsC, EmptyC)):
        return EpsC()
    return StarC(f)


def reduce(d):
    if isinstance(d, (EpsC, EmptyC, CharC)):
        return d

    if isinstance(d, SeqC):
        if isinstance(d.first, EmptyC) or isinstance(d.second, EmptyC):
            return EmptyC()
        if isinstance(d.first, EpsC):
            return d.second
        if isinstance(d.second, EpsC):
            return d.first
        return d

    if isinstance(d, StarC):
        if isinstance(d.first, (EpsC, EmptyC)):
            return EpsC()
        if isinstance(d.first, StarC):
            return d.first
        return d

    if isinstance(d, AltC):
        if isinstance(d.first, EmptyC):
            return d.second
        if isinstance(d.second, EmptyC):
            return d.first
        if isinstance(d.first, EpsC) and nullable(d.second):
            return d.second
        if isinstance(d.second, EpsC) and nullable(d.first):
            return d.first
        if d.first == d.second:
            return d.first
        return d
