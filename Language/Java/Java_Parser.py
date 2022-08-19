from tracemalloc import start
from lark import Lark, Transformer,visitors
global_list = []
info_list = []
def ret_iter(Tree):
    for i in Tree.children:
        if isinstance(i,type(Tree)):
            ret_iter(i)
        else:
            info_list.append(i)
class MyTransformer(visitors.Visitor):
    def assignmentexpression(self, aargs):
        global info_list
        info_list = []
        x = ret_iter(aargs)
        global_list.append(info_list[0])
test = 'int main() { int a = 5; int b = a+10; for(int i = 0;i < 10; i++) printf("%d",i);  return 0; }'
C_parser = Lark.open('Java_Grammar.lark', rel_to=__file__,keep_all_tokens=True,propagate_positions=True)
print(MyTransformer().visit_topdown(C_parser.parse(test)).pretty())
print(global_list)