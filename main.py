from lark import Lark, Transformer
from trellis_builtins import *
import io
from re import findall
import functools
from operator import add

ex = "map { findall { r'(\d)' } b \ first add last . phi int . b } sum . b"

grammar = """\
func: NON_WHITESPACE
partial: func "{" (func | partial | call) "}"
?arg: func | partial | "(" call ")"
trailing1: ("{" func* "}")?
trailing2: func | call
call_nt: call_nt? arg* "." func trailing1 -> call
call_t: call_nt? arg* func "\\\\" trailing2 -> call
?call: call_nt | call_t
?start: call | partial

NON_WHITESPACE: /(?!\\\\)[^\s{}.]+/

%import common.CNAME -> NAME
%import common.WS_INLINE
%import common.SIGNED_NUMBER
%ignore WS_INLINE
%import common.ESCAPED_STRING
"""


parser = Lark(grammar)
for tok in parser.lex(ex):
    print(tok.line, tok.column, repr(tok))

ast = parser.parse(ex)
print(ast.pretty())
print(ast)


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

program = Parser().transform(ast)
print(program(io.StringIO("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""")))
