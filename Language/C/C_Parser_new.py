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
    def declaration(self, items):
        global info_list
        info_list = []
        ret_iter(items)
        print(info_list[1].value)
        if len(info_list[1].value) > 31:
            print("Too long")
        else:
            print("No")
    
        pass


test = open(sys.argv[1], encoding='utf-8').read()
C_parser = Lark.open('C_Grammar.lark', rel_to=__file__,
                     start='translationunit', keep_all_tokens=True, propagate_positions=True)
MyTransformer().visit_topdown(C_parser.parse(test)).pretty()
# print(global_list)
