from tracemalloc import start
from lark import Lark, Transformer, v_args
from lark.indenter import PythonIndenter
collision_grammar = r"""

assignmentexpression: WORD "=" expression
expression: term (("+" | "-") term)*
term: factor (("*" | "/") factor)*
factor: "(" expression ")" | number | WORD
number: /-?[0-9]+/
WORD: /[a-zA-Z_][a-zA-Z0-9_]*/

"""


class MyTransformer(Transformer):
    def expression(self, items):
        return items
    def WORD(self, items):
        return items
    def number(self, items):
        return items
    def factor(self, items):
        return items
    def term(self, items):
        return items
    def for_stmt(self, items):
        print("inssdeee",items)
        for i in items:
            print(i)

test = 'int main() {    int a; a = 12; int b; b = a; int c; c = a + b; printf("%d", c); return 0; }'

p = Lark(collision_grammar, start="assignmentexpression", parser="lalr")
C_parser = Lark.open('C_Grammar.lark', rel_to=__file__,start='translationunit')
print(MyTransformer().transform(C_parser.parse(test)))
