import os
import sys
from lark.lexer import Token
from lark import Lark, visitors, tree

class Utility:
    def __init__(self,lang):
        self.lang = lang
        self.parser_path = os.path.join("../","Language",self.lang,self.lang+"_Parser.py")
        if lang=="c":
            self.utilityObject = cUtilities()
        elif lang=="java":
            self.utilityObject = javaUtilities()
        elif lang=="py":
            self.utilityObject = pythonUtilities()

class getTokens:
    def __init__(self,Tree,token_list):
        if isinstance(Tree,Token):
            token_list.append(Tree.value)
        elif Tree:
            l = Tree.children
            for i in l:  
                getTokens(i,token_list)

class pythonUtilities():
    def __init__(self):
        pass

class cUtilities():
    def __init__(self):
        pass

class javaUtilities():
    def __init__(self):
        pass