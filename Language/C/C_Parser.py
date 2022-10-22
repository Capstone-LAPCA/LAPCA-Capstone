from lark import Lark, visitors
from lark.lexer import Token
import sys
info_list = []
d = {}
line_no = {}
FUNCTIONS = []
class MainTransformer():
    def run(self):
        file = open(sys.argv[1], encoding='utf-8').read()
        #file = 'int main() { int a = 5; int b = a+10; for(int i = 0;i < 10; i++) printf("%d",i);  return 0; }'
        C_parser = Lark.open('C_Grammar.lark', rel_to=__file__,
                             start='translationunit', keep_all_tokens=True, propagate_positions=True)
        CParserActions().visit_topdown(C_parser.parse(file))
        #print(CParserActions().visit_topdown(C_parser.parse(file)).pretty())
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


def getFunctionCalls(Tree,function_calls):
    if Tree.data == "postfixexpression":
        l = Tree.children
        flag = False
        for i in l:
            if isinstance(i,type(Tree)) and i.data == "argumentexpressionlist":
                flag = True
                break
        if flag:
            function_calls.append(l[0].children[0].value)
    l = Tree.children
    for i in l:
        if isinstance(i, type(Tree)):
            getFunctionCalls(i,function_calls)

def getGlobalFunctionCalls(Tree,global_function_calls):
    if Tree.data == "postfixexpression":
        function_calls = []
        getFunctionCalls(Tree,function_calls)
        global_function_calls+=function_calls
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)) and i.data != "functiondefinition":
                getGlobalFunctionCalls(i,global_function_calls)


def getBlockItem(tree,s):
    if isinstance(tree,Token):
        s+=tree.value+' '
    else:
        l = tree.children
        for i in l:
            s+=getBlockItem(i,"")
        d[s] = tree.meta.line
    return s


def getBlockItemList(Tree,block_items):
    if Tree.data == "blockitem":
        block_items.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)):
                getBlockItemList(i,block_items)

def ischild(Tree,child):
    if Tree.data == child:
        return True
    l = Tree.children
    flag=False
    for i in l:
        if isinstance(i, type(Tree)):    
            flag|=ischild(i,child)
    return flag

def getCondition(Tree,condition_list):
    if Tree.data=="iterationstatement" or Tree.data=="selectionstatement":
        condition_list.append(getBlockItem(Tree.children[2],""))
    l = Tree.children
    for i in l:
        if isinstance(i, type(Tree)):    
            getCondition(i,condition_list)

def getTokens(Tree,token_list):
    if isinstance(Tree,Token):
        token_list.append(Tree.value)
    else:
        l = Tree.children
        for i in l:  
            getTokens(i,token_list)

def getExpressionStatements(Tree,expression_statements):
    if Tree.data == "expressionstatement":
        expression_statements.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)):
                getExpressionStatements(i,expression_statements)

def getReturnStatements(Tree,return_statements):
    if Tree.data == "jumpstatement":
        return_statements.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)):
                getReturnStatements(i,return_statements)

class CParserActions(visitors.Visitor):
    def start(self, items):

        pass

    def primaryexpression(self, items):
        LINE_NO = items.meta.line
        cont_pres= items.children[0].value == "continue"

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
        var_decl=False
        LINE_NO=items.meta.line
        if(len(items.children)>1):
            var_decl=True

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
        assign_pres=False
        if(items.children[0].value == "while" and ischild(items.children[2],"assignmentoperator")) or (items.children[0].value == "for" and ischild(items.children[2],"assignmentoperator")):
            LINE_NO = items.meta.line
            assign_pres=True
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list[0]
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        RETURN_STATEMENTS = []
        getReturnStatements(items,RETURN_STATEMENTS)
        pass

    def iterationstatement(self, items):
        assign_pres=False
        if(items.children[0].value == "while" and ischild(items.children[2],"assignmentoperator")) or (items.children[0].value == "for" and ischild(items.children[2],"assignmentoperator")):
            LINE_NO = items.meta.line
            assign_pres=True
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list[0]
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        RETURN_STATEMENTS = []
        getReturnStatements(items,RETURN_STATEMENTS)
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
        GLOBAL_FUNCTION_CALLS=[]
        getGlobalFunctionCalls(items,GLOBAL_FUNCTION_CALLS)
        pass

    def externaldeclaration(self, items):

        pass

    def functiondefinition(self, items):
        d.clear()
        tokens = []
        getTokens(items,tokens)
        FUNCTION_NAME = tokens[1]
        FUNCTION_CALLS = []
        getFunctionCalls(items,FUNCTION_CALLS)
        LINE_NO = items.meta.line
        line_no[FUNCTION_NAME] = LINE_NO
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        pass

    def declarationlist(self, items):

        pass

    def any(self, items):
        
        pass


MainTransformer().run()
