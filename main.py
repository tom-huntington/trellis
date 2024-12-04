from lark import Lark, Transformer, Tree
from trellis_builtins import *
import os
import functools
import re

ex = r"""from re import findall
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
        if token[-1] in (" ", "\n"): token = token[:-1]
        token = rename_illegal.get(token, token)
        return eval(token)
    
    def call(self, args):
        *args_, func, trailing = args
        func = permuted.get(func, func)
        r = func(*args_, *trailing.children)
        return r
    
    def call_p(self, args):
        index, type = next((i, arg) for i, arg in enumerate(args) if isinstance(arg, Tree)) 
        if (type.data == "p"):
            r = b(*args[:index], *args[index+1:])
            return r
        else:
            assert type.data == "star_p"
            assert len(args) == 3
            return bsplat(args[0], args[-1])


def evaluate_code(ex, args):

    while True:
        if m := re.match(r"^from\s+(\w+)\s+import\s+(\w+)\n", ex):
            # print(f"execing: {m.group()}")
            exec(m.group(), globals())
            ex = ex[m.end():]
        else: break
    
    for tok in parser.lex(ex):
        print(tok.line, tok.column, repr(tok))

    ast = parser.parse(ex)
    print(ast.pretty())
    print(ast)


    # ast, = ast.children

    # for tree in imports:
    #     token,  = tree.children
    #     exec(token)
    
    program = Parser().transform(ast)
    program, = program.children
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
    pass
    # evaluate_code(ex, [io.StringIO("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    # Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    # Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    # Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    # Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""")])

    # from operator import sub

    # # evaluate_code("map { splat { sub } }", [[1,2], [3,4], [5,6]])
    # evaluate_code("sub . splat", [[1,2]])

