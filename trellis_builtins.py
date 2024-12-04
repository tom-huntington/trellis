from functools import reduce
import itertools

scan = lambda x, x0, f: itertools.accumulate(x, f, initial=x0)
scan1 = lambda x, f: itertools.accumulate(x, f)

def left(x, y):
    return x

def right(x, y):
    return y

def i(arg):
    return arg

def reverse(xs):
    return tuple(reversed(xs))

def first(xs):
    return xs[0]

def last(xs):
    return xs[-1]

def invoke(f, x):
    return f(x)


def invoke_f(x, f):
    return f(x)

def index(f, x):
    return f[x]

def index_f(x, f):
    return f[x]

def callable(x):
    def callable_result(i):
        return x[i]

    return callable_result

def map_partial_r(f):
    def map_partial_r_inner(*x):
        return map(f, *x)
    return map_partial_r_inner

partials = {
    # map: lambda f: map_partial_r, #lambda *x: map(f, *x),
    scan: lambda f: lambda x, x0: scan(x, x0, f),
    scan1: lambda f: lambda x: scan1(x, f),
}


def map_permuted(x, f):
    return map(f, x)

permuted = {
    map: map_permuted #lambda x, f: map(f, x),
    # map2: lambda x, y, f: map(f, x, y)
}

def bsplat(f, g):
    def bsplat_r(*args):
        fout = f(*args)
        return g(*fout)

    return bsplat_r

def splat(func):
    def splat_ret(args):
        print(args)
        return func(*args)
    return splat_ret

def fanout(*funcs):
    def fanout_r(xs):
        # assert len(funcs) == len(xs)
        return tuple(f(x) for f, x in zip(funcs, xs))
    return fanout_r

def parallel(*funcs):
    def parallel_r(it):
        return (f(i) for f, i in zip(funcs, it))

    return parallel_r

rename_illegal = {
    "&&&": "fanout",
    "***": "parallel"
}


s = lambda f, g: lambda x: f(g(x), x)
sig = lambda f, g: lambda x: g(x, f(x))
phi = lambda f, g, h: lambda x: g(f(x), h(x))

def Phi(f, g, h):
    def Phi_r(x):
        return h(f(x), g(x))
    return Phi_r

def delta(f, g):
    def delta_r(x, y):
        return g(f(x), y)
    return delta_r


def d(f, g):
    def d_r(x, y):
        return f(x, g(y))
    return d_r


def D(g, f):
    def D_r(x, y):
        tmp = g(y)
        return f(x, tmp)
    return D_r


def N(f, g):
    def N_r(x, y):
        return g(x, f(x, y))
    return N_r

Phi1 = lambda f, g, h: lambda x, y: h(f(x, y), g(x, y))
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

def w(f):
    def w_ret(x):
        return f(x, x)
    return w_ret

def S(f, g):
    def S_r(x):
        y = f(x)
        return g(x, y)
    return S_r


def transpose(list_of_lists):
    return zip(*list_of_lists)


def pair(a, b):
    return (a, b)

def map_f(x, f):
    return map(f, x)

def read(x):
    return x.read()

def string(l):
    return ''.join(l)