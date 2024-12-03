from lark import Lark, Transformer
from trellis_builtins import *
import os
import functools


ex = """\
from re import findall
from collections import Counter
from operator import or_
from math import prod
map { findall { r'(\d+) (\w)' } | map { reverse | ( i &&& \ int ) } dict | Counter | Counter.values | prod }
"""

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grammar.lark')) as f:
    grammar = f.read()

parser = Lark(grammar)


class Parser(Transformer):
    def partial(self, args):
        func, arg = args
        if (p := partials.get(func, None)):
            return p(arg)
        return functools.partial(func, arg)

    def fun(self, args):
        token, = args
        token = token.value
        token = rename_illegal.get(token, token)
        return eval(token)
    
    def call(self, args):
        *args_, func, trailing = args
        func = permuted.get(func, func)
        r = func(*args_, *trailing.children)
        return r
    
    def call_p(self, args):
        r = b(*args)
        return r


def evaluate_code(ex, args):
    for tok in parser.lex(ex):
        print(tok.line, tok.column, repr(tok))

    ast = parser.parse(ex)
    print(ast.pretty())
    print(ast)

    *imports, ast = ast.children

    for tree in imports:
        package, a = tree.children
        exec(f"from {package} import {a}", globals())
    
    program = Parser().transform(ast)
    output = program(*args)
    # print_iterable(output)
    return output

def print_iterable(obj):
    if isinstance(obj, (list, tuple, set, dict)):
        print(obj)
    elif hasattr(obj, '__iter__'):
        print(list(obj))
    else:
        print(obj)

if __name__ == "__main__":
    # evaluate_code(ex, [io.StringIO("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    # Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    # Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    # Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    # Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""")])

    from operator import sub

    # evaluate_code("map { splat { sub } }", [[1,2], [3,4], [5,6]])
    evaluate_code("sub . splat", [[1,2]])

