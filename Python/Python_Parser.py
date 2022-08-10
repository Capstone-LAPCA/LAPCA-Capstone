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
    def assignmentexpression(self, items):
        if len(items[0].value)>=5:
            raise Exception("Too long")
        return items
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
p = Lark(collision_grammar, start="assignmentexpression", parser="lalr")
kwargs = dict(postlex=PythonIndenter(), start='file_input')
python_parser2 = Lark.open('Python_Grammar.lark', rel_to=__file__,**kwargs)
MyTransformer().transform(python_parser2.parse("for i in 5:\n    i\n"))
