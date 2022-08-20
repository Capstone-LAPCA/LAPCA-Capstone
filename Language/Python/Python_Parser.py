from lark import Lark, visitors
from lark.indenter import PythonIndenter
import sys
info_list = []

def ret_iter(Tree):
    for i in Tree.children:
        if isinstance(i,type(Tree)):
            ret_iter(i)
        else:
            info_list.append(i)

class MainTransformer():
    def run(self):
        file = open(sys.argv[1], encoding='utf-8').read()
        kwargs = dict(postlex=PythonIndenter(), start='file_input')
        python_parser2 = Lark.open('Python_Grammar.lark', rel_to=__file__, **kwargs,keep_all_tokens=True,propagate_positions=True)
        print(MyTransformer().visit_topdown(python_parser2.parse(file)))

class MyTransformer(visitors.Visitor):
    def single_input(self, items):

        pass
    def file_input(self, items):

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