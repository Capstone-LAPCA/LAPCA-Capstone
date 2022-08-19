from lark import Lark, Transformer

class MyTransformer(Transformer):
    def expression(self, items):
        return items

test = 'int main() {    int a; a = 12; int b; b = a; int c; c = a + b; printf("%d", c); return 0; }'
C_parser = Lark.open('C_Grammar.lark', rel_to=__file__,start='translationunit')
print(MyTransformer().transform(C_parser.parse(test)).pretty())
