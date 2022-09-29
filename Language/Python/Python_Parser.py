from webbrowser import get
from lark import Lark, visitors, tree
from lark.indenter import PythonIndenter
from lark.lexer import Token
import sys
info_list = []
FUNCTIONS = []
line_no = {}
d={}

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
        function_calls.append(Tree.children[0].children[0].children[0].value)
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
        d[s] = Tree.meta.line
    return s


def getBlockItemList(Tree,block_items):
    if Tree.data == "suite" or Tree.data == "if_stmt":
        l = Tree.children
        for i in l:
            block_items.append(getBlockItem(i,"").strip())
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

def checkifelse(Tree):
    count = 0
    if Tree.data=="selectionstatement":
        l = Tree.children
        for i in Tree.children:
            if isinstance(i,Token) and i.value=="if":
                count+=1
            if isinstance(i,Token) and i.value=="else":
                count+=1
    l = Tree.children
    for i in l:
        if isinstance(i, type(Tree)):    
            count+=checkifelse(i)
    return count

def getTokens(Tree,token_list):
    if isinstance(Tree,Token):
        token_list.append(Tree.value)
    else:
        l = Tree.children
        for i in l:  
            getTokens(i,token_list)

def getExpressionStatements(Tree,expression_statements):
    if Tree.data == "simple_stmt":
        expression_statements.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)):
                getExpressionStatements(i,expression_statements)

def getReturnStatements(Tree,return_statements):
    if Tree.data == "return_stmt":
        return_statements.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)):
                getReturnStatements(i,return_statements)

def getBlockItemListObj(Tree,block_items):
    if Tree.data == "suite":
        block_items.append(Tree)
    else:
        l = Tree.children
        for i in l:
            if isinstance(i, type(Tree)):
                getBlockItemListObj(i,block_items)

class MainTransformer():
    def run(self):
        file = open(sys.argv[1], encoding='utf-8').read()
        kwargs = dict(postlex=PythonIndenter(), start='file_input')
        python_parser2 = Lark.open('Python_Grammar.lark', rel_to=__file__, **kwargs,keep_all_tokens=True,propagate_positions=True)
        print(MyTransformer().visit_topdown(python_parser2.parse(file)).pretty())
        #MyTransformer().visit_topdown(python_parser2.parse(file))
        return

class MyTransformer(visitors.Visitor):
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
        FUNCTION_NAME = getFunctionName(items)
        LINE_NO = items.meta.line
        FUNCTION_CALLS = []
        getFunctionCalls(items,FUNCTION_CALLS)
        STATEMENTS = []
        line_no[FUNCTION_NAME] = LINE_NO
        getBlockItemList(items,STATEMENTS)
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

        pass
    def async_stmt(self, items):

        pass
    def if_stmt(self, items):

        pass
    def elifs(self, items):

        pass
    def elif_(self, items):

        pass
    def while_stmt(self, items):
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        STATEMENTOBJ = []
        getBlockItemListObj(items,STATEMENTOBJ)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        RETURN_STATEMENTS = []
        getReturnStatements(items,RETURN_STATEMENTS)
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list[0]
        pass
    def for_stmt(self, items):

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