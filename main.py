from lark import Lark, Transformer
from trellis_builtins import *
import io
import functools

ex = """\
from re import findall
from operator import add
map { findall { r'(\d)' } | first add last . phi | int } | sum
"""

grammar = """\
func: NON_WHITESPACE
partial: func "{" (func | partial | call) "}"
?arg: func | partial | "(" call ")"
trailing1: ("{" func* "}")?
trailing2: _trailing3
_trailing3: func | call
call_nt: call_nt? arg* "." func trailing1 -> call
call_t: call_nt? arg* func "\\\\" trailing2 -> call
call_p: call_nt? arg* "|" _trailing3
?call: call_nt | call_t | call_p
import: "from" NAME "import" NAME "\\n"
start: import* (call | partial)

NON_WHITESPACE: /(?!\\\\)[^\s{}.|]+/

%import common.CNAME -> NAME
%import common.WS
%import common.SIGNED_NUMBER
%ignore WS
%import common.ESCAPED_STRING
"""


parser = Lark(grammar)


class Parser(Transformer):
    def partial(self, args):
        func, arg = args
        if (p := partials.get(func, None)):
            return p(arg)
        return functools.partial(func, arg)

    def func(self, args):
        token, = args 
        return eval(token.value)
    
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
    print(output)
    return output

print(evaluate_code(ex, [io.StringIO("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""")]))