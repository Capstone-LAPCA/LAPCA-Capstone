from lark import Lark, visitors
import sys
info_list = []


class MainTransformer():
    def run(self):
        file = open(sys.argv[1], encoding='utf-8').read()
        #file = 'int main() { int a = 5; int b = a+10; for(int i = 0;i < 10; i++) printf("%d",i);  return 0; }'
        C_parser = Lark.open('C_Grammar.lark', rel_to=__file__,
                             start='translationunit', keep_all_tokens=True, propagate_positions=True)
        MyTransformer().visit_topdown(C_parser.parse(file))
        # print(MyTransformer().visit_topdown(C_parser.parse(file)).pretty())
        return


def ret_iter(Tree, variables):
    if Tree.data == "directdeclarator" and not isinstance(Tree.children[0], type(Tree)):
        return Tree.children[0]
    l = Tree.children
    while len(l):
        i = l.pop()
        if isinstance(i, type(Tree)):
            if i.data == "functiondefinition":
                l.extend(i.children[2:])
                continue
            if i.data == "directdeclarator":
                variables.append(i.children[0])
            l.extend(i.children)


class MyTransformer(visitors.Visitor):
    def start(self, items):

        pass

    def primaryexpression(self, items):

        pass

    def genericselection(self, items):

        pass

    def genericassoclist(self, items):

        pass

    def genericassociation(self, items):

        pass

    def postfixexpression(self, items):

        pass

    def argumentexpressionlist(self, items):

        pass

    def unaryexpression(self, items):

        pass

    def unaryoperator(self, items):

        pass

    def castexpression(self, items):

        pass

    def multiplicativeexpression(self, items):

        pass

    def additiveexpression(self, items):

        pass

    def shiftexpression(self, items):

        pass

    def relationalexpression(self, items):

        pass

    def equalityexpression(self, items):

        pass

    def andexpression(self, items):

        pass

    def exclusiveorexpression(self, items):

        pass

    def inclusiveorexpression(self, items):

        pass

    def logicalandexpression(self, items):

        pass

    def logicalorexpression(self, items):

        pass

    def conditionalexpression(self, items):

        pass

    def assignmentexpression(self, items):

        pass

    def assignmentoperator(self, items):

        pass

    def expression(self, items):

        pass

    def constantexpression(self, items):

        pass

    def declaration(self, items):

        pass

    def declarationspecifiers(self, items):

        pass

    def declarationspecifiers2(self, items):

        pass

    def declarationspecifier(self, items):

        pass

    def initdeclaratorlist(self, items):

        pass

    def initdeclarator(self, items):

        pass

    def storageclassspecifier(self, items):

        pass

    def typespecifier(self, items):

        pass

    def structorunionspecifier(self, items):

        pass

    def structorunion(self, items):

        pass

    def structdeclarationlist(self, items):

        pass

    def structdeclaration(self, items):

        pass

    def specifierqualifierlist(self, items):

        pass

    def structdeclaratorlist(self, items):

        pass

    def structdeclarator(self, items):

        pass

    def enumspecifier(self, items):

        pass

    def enumeratorlist(self, items):

        pass

    def enumerator(self, items):

        pass

    def enumerationconstant(self, items):

        pass

    def atomictypespecifier(self, items):

        pass

    def typequalifier(self, items):

        pass

    def functionspecifier(self, items):

        pass

    def alignmentspecifier(self, items):

        pass

    def declarator(self, items):

        pass

    def directdeclarator(self, items):
        variable = ret_iter(items, [])
        if(not variable):
            return
        LINE_NO = items.meta.line
        pass

    def gccdeclaratorextension(self, items):

        pass

    def gccattributespecifier(self, items):

        pass

    def gccattributelist(self, items):

        pass

    def gccattribute(self, items):

        pass

    def pointer(self, items):

        pass

    def typequalifierlist(self, items):

        pass

    def parametertypelist(self, items):

        pass

    def parameterlist(self, items):

        pass

    def parameterdeclaration(self, items):

        pass

    def identifierlist(self, items):

        pass

    def typename(self, items):

        pass

    def abstractdeclarator(self, items):

        pass

    def directabstractdeclarator(self, items):

        pass

    def typedefname(self, items):

        pass

    def initializer(self, items):

        pass

    def initializerlist(self, items):

        pass

    def designation(self, items):

        pass

    def designatorlist(self, items):

        pass

    def designator(self, items):

        pass

    def staticassertdeclaration(self, items):

        pass

    def statement(self, items):

        pass

    def labeledstatement(self, items):

        pass

    def compoundstatement(self, items):

        pass

    def blockitemlist(self, items):

        pass

    def blockitem(self, items):

        pass

    def expressionstatement(self, items):

        pass

    def selectionstatement(self, items):

        pass

    def iterationstatement(self, items):

        pass

    def forcondition(self, items):

        pass

    def fordeclaration(self, items):

        pass

    def forexpression(self, items):

        pass

    def jumpstatement(self, items):

        pass

    def compilationunit(self, items):

        pass

    def translationunit(self, items):

        pass

    def externaldeclaration(self, items):

        pass

    def functiondefinition(self, items):

        pass

    def declarationlist(self, items):

        pass

    def any(self, items):

        pass


MainTransformer().run()
