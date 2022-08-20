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
    def __init__(self) -> None:
        self.used = set()

    def check(self, name, items):
        global info_list
        if name not in self.used:
            self.used.add(name)
            ret_iter(items)

    def assignmentexpression(self, items):
        self.check('assignmentexpression', items)
        # pass


# test = open(sys.argv[1], encoding='utf-8').read()
test = "int main(){a=5;}"
C_parser = Lark.open('C_Grammar.lark', rel_to=__file__,
                     start='translationunit', keep_all_tokens=True, propagate_positions=True)
MyTransformer().visit_topdown(C_parser.parse(test)).pretty()
# print(global_list)
