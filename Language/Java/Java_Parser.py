from lark import Lark, visitors, tree
import sys
from lark.lexer import Token
import os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from Utils.Utility import Utility, getTokens
global_list = []
info_list = []
STATEMENT_LINE_NO={}
flagIf = False

def ret_iter(Tree, variables):
    if Tree.data == "assign_base" and not isinstance(Tree.children[0], type(Tree)):
        return Tree.children[0]
    l = Tree.children
    while len(l):
        i = l.pop()
        if isinstance(i, type(Tree)):
            if i.data == "literal":
                temp = []
                getTokens(i,temp)
                variables.extend(temp)
            l.extend(i.children)
    return variables[0]

def getFunctionName(Tree):
    l = [Tree]
    while(len(l)):
        i = l.pop()
        if isinstance(i, type(Tree)):
            if i.data == "method_name":
                return i.children[0].children[0].value
            l.extend(i.children)

def getFunctionCalls(Tree,function_calls):
    if Tree.data == "funccall":
        temp = []
        getTokens(Tree,temp)
        function_calls.append("".join(temp[0:temp.index("(")]))
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
            if isinstance(i, type(Tree)) and i.data != "method":
                getGlobalFunctionCalls(i,global_function_calls)

def getBlockItem(Tree,s):
    if isinstance(Tree,Token):
        s+=Tree.value+' '
    elif isinstance(Tree,tree.Tree):
        l = Tree.children
        for i in l:
            s+=getBlockItem(i,"")
        if hasattr(Tree,'meta') and hasattr(Tree.meta,'line'):
            STATEMENT_LINE_NO[s] = Tree.meta.line
    return s


def getBlockItemList(Tree,block_items):
    if Tree.data == "list":
        l = Tree.children
        for i in l:
            if isinstance(i,type(Tree)) and i.data == "stmt": 
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
    if Tree.data == "stmt_base" or Tree.data=="test_stmt" or Tree.data=="single_stmt" or Tree.data=="compound_stmt" or Tree.data=="simple_stmt":
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
    if Tree.data=="test_stmt" or Tree.data=="single_stmt" or Tree.data=="compound_stmt" or Tree.data=="simple_stmt":
        expression_statements.append(getBlockItem(Tree,""))
    else:
        l = Tree.children
        for i in l:
            if isinstance(i,Token) and i.value == "else":
                expression_statements.append("else") 
            if isinstance(i, type(Tree)):
                if i.data == "if_stmt" or i.data=="else_stmt":
                    expression_statements.append("else")
                getExpressionStatementsInsideIf(i,expression_statements)

def getFunctionParams(Tree, param_list):
    if Tree.data == "parameter_name":
        param_list.append(getBlockItem(Tree,""))
    else:
        for i in Tree.children:
            if isinstance(i,type(Tree)):
                getFunctionParams(i,param_list)

class MainTransformer():
    def run(self):
        file = open(sys.argv[1], encoding='utf-8').read()
        Java_parser = Lark.open('Java_Grammar.lark', start="clazz",rel_to=__file__, keep_all_tokens=True, propagate_positions=True)
        javaParserActions().visit_topdown(Java_parser.parse(file))
        #print(javaParserActions().visit_topdown(Java_parser.parse(file)).pretty())
        return

class javaParserActions(visitors.Visitor):
    def modifier(self, items):

        pass
        
    def package_stmt(self, items):

        pass
    def imports(self, items):

        pass
    def import_stmt(self, items):

        pass
    def annotations(self, items):

        pass
    def annotation(self, items):

        pass
    def anno_args(self, items):

        pass
    def anno_arg_kv(self, items):

        pass
    def anno_arg_list(self, items):

        pass
    def anno_arg_base_list(self, items):

        pass
    def anno_arg_base(self, items):

        pass
    def fields(self, items):

        pass
    def field(self, items):

        pass
    def field_annotation(self, items):

        pass
    def enum_class_elem(self, items):

        pass
    def enum_field(self, items):

        pass
    def enum_field_modifiers(self, items):

        pass
    def enum_field_name(self, items):

        pass
    def enum_field_body(self, items):

        pass
    def enum_elems(self, items):

        pass
    def enum_elem(self, items):

        pass
    def enum_elem_name(self, items):

        pass
    def enum_elem_args(self, items):

        pass
    def enum_elem_body(self, items):

        pass
    def method(self, items):
        FUNCTION_NAME = getFunctionName(items)
        LINE_NO = items.meta.line
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        FUNCTION_CALLS = []
        getFunctionCalls(items,FUNCTION_CALLS)
        FUNCTION_PARAMS = []
        getFunctionParams(items,FUNCTION_PARAMS)
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass
    def method_annotations(self, items):

        pass
    def method_modifiers(self, items):

        pass
    def method_return(self, items):

        pass
    def method_name(self, items):

        pass
    def method_parameters(self, items):

        pass
    def method_throws(self, items):

        pass
    def method_body(self, items):

        pass
    def classes(self, items):

        pass
    def block(self, items):

        pass
    def block_modifier(self, items):

        pass
    def clazz(self, items):
        GLOBAL_FUNCTION_CALLS=[]
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        getGlobalFunctionCalls(items,GLOBAL_FUNCTION_CALLS)
        pass
    def class_package(self, items):

        pass
    def class_imports(self, items):

        pass
    def class_comment(self, items):

        pass
    def class_annotations(self, items):

        pass
    def class_modifier(self, items):

        pass
    def class_identity(self, items):

        pass
    def class_identifier(self, items):

        pass
    def class_def_generic(self, items):

        pass
    def class_extends(self, items):

        pass
    def class_interfaces(self, items):

        pass
    def class_throws(self, items):

        pass
    def class_body(self, items):

        pass
    def stmt(self, items):

        pass
    def stmt_base(self, items):

        pass
    def expr_stmt(self, items):

        pass
    def simple_stmt(self, items):

        pass
    def test_stmt(self, items):

        pass
    def assign_modifier(self, items):

        pass
    def assign_type(self, items):

        pass
    def assign_mul(self, items):
        LINE_NO=items.meta.line
        var_list=items.children

        pass
    def assign_base(self, items):
        variable = ret_iter(items, [])
        if(not variable):
            return 
        LINE_NO = items.meta.line
        
        pass
    def break_stmt(self, items):

        pass
    def continue_stmt(self, items):
        cont_pres=True
        LINE_NO=items.meta.line

        pass
    def return_stmt(self, items):

        pass
    def throw_stmt(self, items):

        pass
    def assert_stmt(self, items):

        pass
    def name_base(self, items):

        pass
    def namearr(self, items):

        pass
    def arr_operation(self, items):

        pass
    def test_stmt_inline(self, items):

        pass
    def compound_stmt(self, items):
        STATEMENTS = []
        LINE_NO = items.meta.line
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = ""
        ITERATION = ""
        if items.children[0].data == "while_stmt":
            ITERATION_CONDITION = condition_list
            ITERATION = "while"
        elif items.children[0].data == "for_stmt":
            ITERATION = "for"
            ITERATION_CONDITION = condition_list
        else :
            ITERATION = items.children[0].data
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass
    def synchronized_stmt(self, items):

        pass
    def try_stmt(self, items):

        pass
    def try_with(self, items):

        pass
    def try_body(self, items):

        pass
    def catch_finally_stmt(self, items):

        pass
    def catches_stmt(self, items):

        pass
    def catch_stmt(self, items):

        pass
    def catch_ex(self, items):

        pass
    def catch_ex_type(self, items):

        pass
    def finally_stmt(self, items):

        pass
    def do_while_stmt(self, items):
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass
    def while_stmt(self, items):
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = ""
        if len(condition_list) > 0:
            ITERATION_CONDITION = condition_list[0]
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass
    def for_stmt(self, items):
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)
        EXP_STATEMENTS = []
        getExpressionStatements(items,EXP_STATEMENTS)
        condition_list = []
        getCondition(items,condition_list)
        ITERATION_CONDITION = condition_list
        EXP_STATEMENTS_INSIDE_ALL_IF = []
        getExpressionStatementsInsideAllIf(items,EXP_STATEMENTS_INSIDE_ALL_IF)
        pass
    def for_test(self, items):

        pass
    def for_test_var(self, items):

        pass
    def for_test_con(self, items):

        pass
    def for_test_expr(self, items):

        pass
    def switch_stmt(self, items):
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        LINE_NO = items.meta.line
        pass
    def case_stmts(self, items):

        pass
    def case_suit(self, items):

        pass
    def case_key(self, items):

        pass
    def case_type(self, items):

        pass
    def if_stmt(self, items):
        ALL_TOKENS = []
        getTokens(items,ALL_TOKENS)
        LINE_NO = items.meta.line
        FUNCTION_CALLS = []
        getFunctionCalls(items,FUNCTION_CALLS)
        STATEMENTS = []
        getBlockItemList(items,STATEMENTS)

        pass
    def elif_stmt(self, items):

        pass
    def else_stmt(self, items):

        pass
    def single_stmt(self, items):

        pass
    def suit(self, items):

        pass
    def test(self, items):

        pass
    def lambda_expr(self, items):

        pass
    def lambda_param(self, items):

        pass
    def lambda_body(self, items):

        pass
    def or_test(self, items):

        pass
    def and_test(self, items):

        pass
    def not_test(self, items):

        pass
    def comparison(self, items):

        pass
    def expr(self, items):

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
    def binary_bf(self, items):

        pass
    def power(self, items):

        pass
    def cast_expr(self, items):

        pass
    def new_expr(self, items):

        pass
    def atom_expr(self, items):

        pass
    def atom(self, items):

        pass
    def chain_generic(self, items):

        pass
    def class_type(self, items):

        pass
    def class_ellipsis(self, items):

        pass
    def class_generic(self, items):

        pass
    def generic_type(self, items):

        pass
    def generic_extends_list(self, items):

        pass
    def generic_extends(self, items):

        pass
    def class_type_list(self, items):

        pass
    def cast_type(self, items):

        pass
    def arguments(self, items):

        pass
    def argvalue(self, items):

        pass
    def _binary_op(self, items):

        pass
    def _add_op(self, items):

        pass
    def _shift_op(self, items):

        pass
    def _mul_op(self, items):

        pass
    def _comp_op(self, items):

        pass
    def _assign_op(self, items):

        pass
    def parameters(self, items):

        pass
    def parameter(self, items):

        pass
    def parameter_modifier(self, items):

        pass
    def parameter_name(self, items):

        pass
    def comment_nouse(self, items):

        pass
    def comment(self, items):

        pass
    def comment_base(self, items):

        pass
    def comment_inline(self, items):

        pass
    def return_type(self, items):

        pass
    def path(self, items):

        pass
    def name(self, items):

        pass
    def class_name(self, items):

        pass
    def dotted_name(self, items):

        pass
    def star(self, items):

        pass
    def primary(self, items):

        pass
    def string(self, items):

        pass
    def char(self, items):

        pass
    def number(self, items):

        pass
    def number_base(self, items):

        pass
    def boolean(self, items):

        pass
    def true(self, items):

        pass
    def false(self, items):

        pass
    def null(self, items):

        pass
    def new(self, items):

        pass
    def ellipsis(self, items):

        pass
    def arr_suffix(self, items):

        pass
    def primary_type(self, items):

        pass
MainTransformer().run()