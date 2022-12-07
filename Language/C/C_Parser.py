from lark import Lark, visitors
from lark.lexer import Token
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from Utils.Utility import Utility, getTokens
info_list = []
STATEMENT_LINE_NO = {}
flagIf = False
map_state_to_code = {}

class MainTransformer():
    def __init__(self,temp,test_file_path):
        global map_state_to_code
        map_state_to_code = temp
        self.test_file_path = test_file_path
    def run(self):
        file = open(self.test_file_path, encoding='utf-8').read()
        #file = 'int main() { int a = 5; int b = a+10; for(int i = 0;i < 10; i++) printf("%d",i);  return 0; }'
        exec(map_state_to_code["before"])
        C_parser = Lark.open('C_Grammar.lark', rel_to=__file__,
                             start='translationunit', keep_all_tokens=True, propagate_positions=True)
        CParserActions().visit_topdown(C_parser.parse(file))
        exec(map_state_to_code["after"])
        # print(CParserActions().visit_topdown(C_parser.parse(file)).pretty())
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
            STATEMENT_LINE_NO[s] = tree.meta.line
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
    if Tree.data=="while_stmt" or Tree.data =="for_stmt" or Tree.data=="if_stmt" or Tree.data=="switch_stmt":
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
    if Tree.data == "if_stmt":
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
    if Tree.data == "if_stmt":
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

def getFunctionParams(Tree, param_list):
    if Tree.data == "parameterdeclaration":
        param_list.append(getBlockItem(Tree,""))
    else:
        for i in Tree.children:
            if isinstance(i,type(Tree)):
                getFunctionParams(i,param_list)

class CParserActions(visitors.Visitor):
    def for_stmt(self, items):
        LINE_NO=items.meta.line
        condition_list = []
        ITERATION = "for"
        getCondition(items,condition_list)
        ITERATION_CONDITION = ""
        if len(condition_list):
            ITERATION_CONDITION = condition_list[0]
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        exec(map_state_to_code["for_stmt"])
        pass

    def while_stmt(self, items):
        LINE_NO=items.meta.line
        condition_list = []
        ITERATION = "while"
        getCondition(items,condition_list)
        ITERATION_CONDITION = ""
        if len(condition_list):
            ITERATION_CONDITION = condition_list[0]
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        exec(map_state_to_code["while_stmt"])
        pass

    def switch_stmt(self, items):
        LINE_NO = items.meta.line
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        exec(map_state_to_code["switch_stmt"])
        pass
    def start(self, items):
        LINE_NO = items.meta.line
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        pass

    def primaryexpression(self, items):
        LINE_NO = items.meta.line
        cont_pres= items.children[0].value == "continue"
        exec(map_state_to_code["primaryexpression"])
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
        LINE_NO=items.meta.line
        var_list=items.children
        exec(map_state_to_code["initdeclaratorlist"])
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
        exec(map_state_to_code["directdeclarator"])
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
    
    def if_stmt(self, items):
        condition_list = []
        ALL_TOKENS = []
        LINE_NO = items.meta.line
        getTokens(items,ALL_TOKENS)
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        exec(map_state_to_code["if_stmt"])
        pass

    def selectionstatement(self, items):
        condition_list = []
        LINE_NO = items.meta.line
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        pass

    def iterationstatement(self, items):
        LINE_NO=items.meta.line
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        condition_list = []
        ITERATION = ""
        if items.children[0].data == "while_stmt":
            ITERATION = "while"
        elif items.children[0].data == "for_stmt":
            ITERATION = "for"
        else:
            ITERATION = items.children[0].data
        getCondition(items,condition_list)
        ASSIGN_COND = ""
        if len(condition_list) > 0:
            ASSIGN_COND = condition_list[0].split(';')
            if len(ASSIGN_COND) > 1:
                ASSIGN_COND = ASSIGN_COND[1]
            else:
                ASSIGN_COND = ASSIGN_COND[0]
        ITERATION_CONDITION = ""
        if len(condition_list):
            ITERATION_CONDITION = condition_list[0]
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        exec(map_state_to_code["iterationstatement"])
        pass

    def forcondition(self, items):
        LINE_NO=items.meta.line
        pass

    def fordeclaration(self, items):
        LINE_NO=items.meta.line
        pass

    def forexpression(self, items):
        LINE_NO=items.meta.line
        pass

    def jumpstatement(self, items):

        pass

    def compilationunit(self, items):

        pass

    def translationunit(self, items):
        GLOBAL_FUNCTION_CALLS=[]
        LINE_NO=items.meta.line
        getGlobalFunctionCalls(items,GLOBAL_FUNCTION_CALLS)
        exec(map_state_to_code["translationunit"])
        pass

    def externaldeclaration(self, items):

        pass

    def functiondefinition(self, items):
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        FUNCTION_NAME = ALL_TOKENS[ALL_TOKENS.index("(")-1]
        FUNCTION_CALLS = []
        FUNCTION_PARAMS = []
        getFunctionParams(items,FUNCTION_PARAMS)
        getFunctionCalls(items,FUNCTION_CALLS)
        LINE_NO = items.meta.line
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        exec(map_state_to_code["functiondefinition"])
        pass

    def declarationlist(self, items):

        pass

    def any(self, items):
        
        pass


# MainTransformer().run()