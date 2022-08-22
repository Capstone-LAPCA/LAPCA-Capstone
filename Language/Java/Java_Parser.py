from tracemalloc import start
from lark import Lark, Transformer, visitors
import sys
global_list = []
info_list = []


def ret_iter(Tree):
    for i in Tree.children:
        if isinstance(i, type(Tree)):
            ret_iter(i)
        else:
            info_list.append(i)


class MyTransformer(visitors.Visitor):
    def assignmentexpression(self, items):
        #if len(var) > 31:
        print("Too long")
        pass


test = open(sys.argv[1], encoding='utf-8').read()
#test = 'public class Test { public static void main(String[] args) { int a = 5; int b = a+10; for(int i = 0;i < 10; i++) {System.out.println(i);}  return 0; } }'
Java_parser = Lark.open('Java_Grammar.lark', start="clazz",
                     rel_to=__file__, keep_all_tokens=True, propagate_positions=True)
print(MyTransformer().visit_topdown(Java_parser.parse(test)).pretty())
print(global_list)
