from webbrowser import get
from lark import Lark, visitors, tree
from lark.indenter import PythonIndenter
from lark.lexer import Token
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from Utils.Utility import Utility, getTokens
info_list = []
FUNCTIONS = []
line_no = {}
d = {}
flagIf = False

def ret_iter(Tree,variables):
    if Tree.data == "assign" and not isinstance(Tree.children[0], type(Tree)):
        return Tree.children[0]
    l = Tree.children
    while len(l):
        i = l.pop()
        
        if isinstance(i, type(Tree)):
            if i.data == "simple_stmt":  
                l.extend(i.children[2:])
                continue
            if i.data == "name":
                variables.append(i.children[0].value)
            l.extend(i.children)
    return variables[0]

def getFunctionName(Tree):
    if Tree.data == "funcdef":
        l = Tree.children
        for i in l:
            if isinstance(i,type(Tree)) and i.data == "name":
                return i.children[0]

def getFunctionCalls(Tree,function_calls):
    if Tree.data == "funccall":
        temp = []
        getTokens(Tree,temp)
        indices = []
        for idx, value in enumerate(temp):
            if value == '(':
                indices.append(idx)
        for i in indices:
            function_calls.append(temp[i-1])
    l = Tree.children
    for i in l:
        if isinstance(i, type(Tree)):
            getFunctionCalls(i,function_calls)

def getGlobalFunctionCalls(Tree,global_function_calls):
    if Tree.data == "funccall":
        function_calls = []
        getFunctionCalls(Tree,function_calls)
        global_function_calls+=function_calls
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)) and i.data != "funcdef":
                getGlobalFunctionCalls(i,global_function_calls)

def getBlockItem(Tree,s):
    if isinstance(Tree,Token):
        s+=Tree.value+' '
    elif isinstance(Tree,tree.Tree):
        l = Tree.children
        for i in l:
            s+=getBlockItem(i,"")
        if hasattr(Tree,'meta') and hasattr(Tree.meta,'line'):
            d[s] = Tree.meta.line
    return s


def getBlockItemList(Tree,block_items):
    if Tree.data == "suite":
        l = Tree.children
        for i in l:
            if getBlockItem(i,"").strip() != "":
                block_items.append(getBlockItem(i,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)):
                getBlockItemList(i,block_items)

def getCondition(Tree,condition_list):
    if Tree.data=="comparison":
        condition_list.append(getBlockItem(Tree,""))
    l = Tree.children
    for i in l:
        if isinstance(i, type(Tree)):    
            getCondition(i,condition_list)

def getExpressionStatements(Tree,expression_statements):
    if Tree.data == "simple_stmt":
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
    l = Tree.children
    for i in l:
        if isinstance(i, type(Tree)):
            getExpressionStatementsInsideAllIf(i,expression_statements)

def getExpressionStatementsInsideIf(Tree,expression_statements):
    global flagIf
    if Tree.data == "if_stmt":
        if flagIf:
            return None
        else:
            flagIf = True
    if Tree.data=="simple_stmt" or Tree.data =="compound_stmt" or Tree.data=="stmt":
        expression_statements.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i,Token) and i.value == "else":
                expression_statements.append("else") 
            if isinstance(i, type(Tree)):
                if i.data == "if_stmt" or i.data=="elifs":
                    expression_statements.append("else")
                getExpressionStatementsInsideIf(i,expression_statements)

def getFunctionParams(Tree, param_list):
    for i in Tree.children:
        if isinstance(i,type(Tree)) and i.data == "parameters":
                for child in i.children:
                    if isinstance(child,type(Tree)):
                        param_list.append(getBlockItem(child,""))

class MainTransformer():
    def run(self):
        file = open(sys.argv[1], encoding='utf-8').read()
        file+="\n"
        kwargs = dict(postlex=PythonIndenter(), start='file_input')
        python_parser2 = Lark.open('Python_Grammar.lark', rel_to=__file__, **kwargs,keep_all_tokens=True,propagate_positions=True)
        # print(pythonParserActions().visit_topdown(python_parser2.parse(file)).pretty())
        pythonParserActions().visit_topdown(python_parser2.parse(file))
        return

class pythonParserActions(visitors.Visitor):
    def single_input(self, items):

        pass
    def file_input(self, items):
        GLOBAL_FUNCTION_CALLS=[]
        getGlobalFunctionCalls(items,GLOBAL_FUNCTION_CALLS)
        pass
    def eval_input(self, items):

        pass
    def decorator(self, items):

        pass
    def decorators(self, items):

        pass
    def decorated(self, items):

        pass
    def async_funcdef(self, items):

        pass
    def funcdef(self, items):
        FUNCTION_PARAMS = [] 
        getFunctionParams(items,FUNCTION_PARAMS)
        FUNCTION_NAME = getFunctionName(items)
        LINE_NO = items.meta.line
        FUNCTION_CALLS = []
        getFunctionCalls(items,FUNCTION_CALLS)
        STATEMENTS = []
        line_no[FUNCTION_NAME] = LINE_NO
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        
        pass
    def parameters(self, items):

        pass
    def starparams(self, items):

        pass
    def starparam(self, items):

        pass
    def starguard(self, items):

        pass
    def poststarparams(self, items):

        pass
    def kwparams(self, items):

        pass
    def paramvalue(self, items):

        pass
    def typedparam(self, items):

        pass
    def lambdef(self, items):

        pass
    def lambdef_nocond(self, items):

        pass
    def lambda_params(self, items):

        pass
    def lambda_paramvalue(self, items):

        pass
    def lambda_starparams(self, items):

        pass
    def lambda_kwparams(self, items):

        pass
    def stmt(self, items):

        pass
    def simple_stmt(self, items):

        pass
    def small_stmt(self, items):

        pass
    def expr_stmt(self, items):

        pass
    def assign_stmt(self, items):

        pass
    def annassign(self, items):

        pass
    def assign(self, items):
        variable = ret_iter(items, [])
        if(not variable):
            return 
        LINE_NO = items.meta.line
        
        pass
    def augassign(self, items):

        pass
    def augassign_op(self, items):

        pass
    def testlist_star_expr(self, items):

        pass
    def del_stmt(self, items):

        pass
    def pass_stmt(self, items):

        pass
    def flow_stmt(self, items):

        pass
    def break_stmt(self, items):

        pass
    def continue_stmt(self, items):   
        cont_pres=True    
        LINE_NO=items.meta.line

        pass
    def return_stmt(self, items):

        pass
    def yield_stmt(self, items):

        pass
    def raise_stmt(self, items):

        pass
    def import_stmt(self, items):

        pass
    def import_name(self, items):

        pass
    def import_from(self, items):

        pass
    def dots(self, items):

        pass
    def import_as_name(self, items):

        pass
    def dotted_as_name(self, items):

        pass
    def import_as_names(self, items):

        pass
    def dotted_as_names(self, items):

        pass
    def dotted_name(self, items):

        pass
    def global_stmt(self, items):

        pass
    def nonlocal_stmt(self, items):

        pass
    def assert_stmt(self, items):

        pass
    def compound_stmt(self, items):
        STATEMENTS = []
        LINE_NO = items.meta.line
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = ""
        ITERATION = ""
        if items.children[0].data == "while_stmt":
            ITERATION_CONDITION = getCondition(items.children[0],[])
            ITERATION = "while"
        elif items.children[0].data == "for_stmt":
            ITERATION = "for"
        else :
            ITERATION = items.children[0].data
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass
    def async_stmt(self, items):

        pass
    def if_stmt(self, items):
        LINE_NO = items.meta.line
        FUNCTION_CALLS = []
        getFunctionCalls(items,FUNCTION_CALLS)
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        pass
    def elifs(self, items):

        pass
    def elif_(self, items):

        pass
    def while_stmt(self, items):
        STATEMENTS = []
        LINE_NO = items.meta.line
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass
    def for_stmt(self, items):
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = ""
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass
    def try_stmt(self, items):

        pass
    def except_clauses(self, items):

        pass
    def except_clause(self, items):

        pass
    def with_stmt(self, items):

        pass
    def with_items(self, items):

        pass
    def with_item(self, items):

        pass
    def match_stmt(self, items):
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        LINE_NO = items.meta.line
        pass
    def case(self, items):

        pass
    def pattern(self, items):

        pass
    def as_pattern(self, items):

        pass
    def or_pattern(self, items):

        pass
    def closed_pattern(self, items):

        pass
    def literal_pattern(self, items):

        pass
    def inner_literal_pattern(self, items):

        pass
    def attr_pattern(self, items):

        pass
    def name_or_attr_pattern(self, items):

        pass
    def mapping_item_pattern(self, items):

        pass
    def sequence_pattern(self, items):

        pass
    def sequence_item_pattern(self, items):

        pass
    def class_pattern(self, items):

        pass
    def arguments_pattern(self, items):

        pass
    def pos_arg_pattern(self, items):

        pass
    def keyws_arg_pattern(self, items):

        pass
    def keyw_arg_pattern(self, items):

        pass
    def suite(self, items):

        pass
    def test(self, items):

        pass
    def assign_expr(self, items):

        pass
    def test_nocond(self, items):

        pass
    def or_test(self, items):

        pass
    def and_test(self, items):

        pass
    def not_test_(self, items):

        pass
    def comparison(self, items):

        pass
    def star_expr(self, items):

        pass
    def expr(self, items):

        pass
    def or_expr(self, items):

        pass
    def xor_expr(self, items):

        pass
    def and_expr(self, items):

        pass
    def shift_expr(self, items):

        pass
    def arith_expr(self, items):

        pass
    def term(self, items):

        pass
    def factor(self, items):

        pass
    def _unary_op(self, items):

        pass
    def _add_op(self, items):

        pass
    def _shift_op(self, items):

        pass
    def _mul_op(self, items):

        pass
    def comp_op(self, items):

        pass
    def power(self, items):

        pass
    def await_expr(self, items):

        pass
    def atom_expr(self, items):

        pass
    def atom(self, items):

        pass
    def string_concat(self, items):

        pass
    def testlist_comp(self, items):

        pass
    def tuple_inner(self, items):

        pass
    def test_or_star_expr(self, items):

        pass
    def subscriptlist(self, items):

        pass
    def subscript(self, items):

        pass
    def sliceop(self, items):

        pass
    def exprlist(self, items):

        pass
    def testlist(self, items):

        pass
    def testlist_tuple(self, items):

        pass
    def dict_exprlist(self, items):

        pass
    def key_value(self, items):

        pass
    def set_exprlist(self, items):

        pass
    def classdef(self, items):

        pass
    def arguments(self, items):

        pass
    def starargs(self, items):

        pass
    def stararg(self, items):

        pass
    def kwargs(self, items):

        pass
    def argvalue(self, items):

        pass
    def comp_fors(self, items):

        pass
    def comp_for(self, items):

        pass
    def comp_if(self, items):

        pass
    def encoding_decl(self, items):

        pass
    def yield_expr(self, items):

        pass
    def number(self, items):

        pass
    def string(self, items):

        pass
    def name(self, items):

        pass

MainTransformer().run()