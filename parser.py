def nullable(c):
    if isinstance(c, Empty) or isinstance(c, Char):
        return False
    if isinstance(c, Eps) or isinstance(c, Star):
        return True
    if isinstance(c, Alt):
        return nullable(c.first) or nullable(c.second)
    if isinstance(c, Seq):
        return nullable(c.first) and nullable(c.second)
    raise Exception("Input Error")


class Derives(object):
    def __call__(self, w, f=None):
        if f is None:
            f = self

        if w == "":
            return nullable(f)

        if isinstance(f, Empty):
            return False

        return self.__call__(w[1:], self.derivative(w[0], f))

    def derivative(self, c, o=None):
        if o is None:
            o = self

        if isinstance(o, Empty):
            return Empty()

        if isinstance(o, Eps):
            return Empty()

        if isinstance(o, Char):
            if o.first == c:
                return Eps()
            return Empty()

        if isinstance(o, Star):
            return Seq(o.first.derivative(c), o)

        if isinstance(o, Alt):
            if isinstance(o.first, Empty):
                return o.second.derivative(c)
            if isinstance(o.second, Empty):
                return o.first.derivative(c)
            return Alt(o.first.derivative(c), o.second.derivative(c))

        if isinstance(o, Seq):
            left_derivative = Seq(o.first.derivative(c), o.second)
            if nullable(o.first):
                return Alt(left_derivative, o.second.derivative(c))
            return left_derivative


class Empty(Derives):
    def __init__(self, *args): pass

    def __eq__(self, other):
        if not isinstance(other, Empty):
            return False
        return True

    def __str__(self): return "Empty"


class Eps(Derives):
    def __init__(self, *args): pass

    def __eq__(self, other):
        if not isinstance(other, Eps):
            return False
        return True

    def __str__(self): return "Eps"


class Char(Derives):
    def __init__(self, c):
        self.first = c

    def __eq__(self, other):
        if not isinstance(other, Char):
            return False
        return self.first == other.first

    def __str__(self): return "'{}'".format(self.first)


class Seq(Derives):
    def __init__(self, f, s, *args):
        if len(args) > 0:
            if isinstance(f, Empty):
                self.first = Empty()
                self.second = Empty()
            else:
                self.first = f
                self.second = Seq(s, args[0], *args[1:])
        else:
            if isinstance(f, Empty) or isinstance(s, Empty):
                self.first = Empty()
                self.second = Empty()
            else:
                self.first = f
                self.second = s

    def __eq__(self, other):
        if not isinstance(other, Seq):
            return False
        return (self.first == other.first) & (self.second == other.second)

    def __str__(self):
        return "(Seq {} {})".format(self.first, self.second)


class Alt(Derives):
    def __init__(self, f, s, *args):
        if len(args) > 0:
            if f == s:
                self.first = Empty()
            else:
                self.first = f
            self.second = Alt(s, args[0], *args[1:])
        else:
            if f == s:
                self.first = Empty()
            else:
                self.first = f
            self.second = s

    def __eq__(self, other):
        if not isinstance(other, Alt):
            return False
        return (self.first == other.first) & (self.second == other.second)

    def __str__(self):
        return "(Alt {} {})".format(self.first, self.second)


class Star(Derives):
    def __init__(self, f):
        if isinstance(f, Star):
            self.first = f.first
        else:
            self.first = f

    def __eq__(self, other):
        if not isinstance(other, Star):
            return False
        return self.first == other.first

    def __str__(self):
        return "(Star {})".format(self.first)


'''
Что если сделать функцию reduce, которая принимает класс и уменьшает его
'''
