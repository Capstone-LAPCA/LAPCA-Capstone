from lark import Lark, visitors
from lark.lexer import Token
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from Utils.Utility import Utility, getTokens
info_list = []
d = {}
line_no = {}
FUNCTIONS = []
flagIf = False

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
        return Tree.children[0].value
    l = Tree.children
    for i in l:
        if isinstance(i, type(Tree)):
            ret_iter(i, variables)


def getFunctionCalls(Tree,function_calls):
    if Tree.data == "postfixexpression":
        temp = []
        getTokens(Tree,temp)
        if len(temp)>1 and temp[1] == '(': 
            function_calls.append(temp[0])
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
        if hasattr(tree,'meta') and hasattr(tree.meta,'line'):
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

def getExpressionStatements(Tree,expression_statements):
    if Tree.data == "expressionstatement":
        expression_statements.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)):
                getExpressionStatements(i,expression_statements)

def getExpressionStatementsInsideAllIf(Tree,expression_statements):
    global flagIf
    if Tree.data == "selectionstatement":
        expr = []
        getExpressionStatementsInsideIf(Tree,expr)
        if "else" in expr:
            start = 0
            while start<len(expr) and "else" in expr[start:]:
                ind = expr.index("else",start)
                if len(expr[start:ind]):
                    expression_statements.append(expr[start:ind])
                start = ind+1
            if len(expr[start:]):
                expression_statements.append(expr[start:])
        elif len(expr):
            expression_statements.append(expr)
        flagIf = False
    if Tree.data == "declaration":
        tok = []
        getTokens(Tree,tok)
        if tok[0] == 'else':
            expression_statements.append(["".join(tok[1:])])
    l = Tree.children
    for i in l:
        if isinstance(i, type(Tree)):
            getExpressionStatementsInsideAllIf(i,expression_statements)

def getExpressionStatementsInsideIf(Tree,expression_statements):
    global flagIf
    if Tree.data == "selectionstatement":
        if flagIf:
            return
        else:
            flagIf = True
    if Tree.data == "expressionstatement" or Tree.data=="blockitem" or Tree.data=="jumpstatement":
        expression_statements.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i,Token) and i.value == "else":
                expression_statements.append("else")
            if isinstance(i, type(Tree)):
                getExpressionStatementsInsideIf(i,expression_statements)

class CParserActions(visitors.Visitor):
    def while_rule(self,items):

        pass
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
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        pass

    def iterationstatement(self, items):
        LINE_NO=items.meta.line
        condition_list = []
        ITERATION = ""
        if items.children[0].value == "while":
            ITERATION = "while"
        elif items.children[0].value == "for":
            ITERATION = "for"
        else:
            ITERATION = items.children[0].value
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
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
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass

    def declarationlist(self, items):

        pass

    def any(self, items):
        
        pass


MainTransformer().run()
