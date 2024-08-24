from functools import reduce
import itertools

scan = lambda x, x0, f: itertools.accumulate(x, f, initial=x0)
scan1 = lambda x, f: itertools.accumulate(x, f)
def first(xs):
    return xs[0]

def last(xs):
    return xs[-1]

partials = {
    map: lambda f: lambda x: map(f, x),
    scan: lambda f: lambda x, x0: scan(x, x0, f),
    scan1: lambda f: lambda x: scan1(x, f),
}
permuted = {
    map: lambda x, f: map(f, x)
}



s = lambda f, g: lambda x: f(g(x), x)
sig = lambda f, g: lambda x: g(x, f(x))
phi = lambda f, g, h: lambda x: g(f(x), h(x))
Phi = lambda f, g, h: lambda x: h(f(x), g(x))
def b(f, *fs):
    def b_ret(*args):
        def b_inner(v, f_):
            return f_(v)
        initial = f(*args)
        return reduce(b_inner, fs, initial)
    return b_ret

def d2(f, g, h):
    def d2_ret(x, y):
        return g(f(x), h(y))
    return d2_ret

def s(f):
    def s_ret(x):
        return f(x, x)
    return s_ret


