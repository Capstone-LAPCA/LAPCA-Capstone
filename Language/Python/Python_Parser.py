from tracemalloc import start
from lark import Lark, Transformer, v_args, Tree
from lark.indenter import PythonIndenter
import sys


class MyTransformer(Transformer):
    def assign(self, items):

        pass

    def name(self, items):
        return items[0]


class MainTransformer(Transformer):
    def run(self):
        file = open(sys.argv[1], encoding='utf-8').read()
        kwargs = dict(postlex=PythonIndenter(), start='file_input')
        python_parser2 = Lark.open(
            'Python_Grammar.lark', rel_to=__file__, **kwargs)
        MyTransformer().transform(python_parser2.parse(file))


MainTransformer().run()
