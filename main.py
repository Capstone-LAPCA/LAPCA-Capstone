from multiprocessing.spawn import import_main_path
import sys
import os
# from Language.Python.Make_Parser import PythonMakeParser
# from Language.C.Make_Parser import CMakeParser
# from Language.Java.Make_Parser import JavaMakeParser
from makeParser import Parser


def factory(lang, formal_structures):
    if lang == "py":
        Parser(lang, formal_structures, "Language/Python/Python_Parser.py",
               "Language/Python/Python_Parser_new.py")
        os.system("python Language/Python/Python_Parser_new.py "+sys.argv[2])
    elif lang == "c":
        Parser(lang, formal_structures, "Language/C/C_Parser.py",
               "Language/C/C_Parser_new.py")
        os.system("python Language/C/C_Parser_new.py "+sys.argv[2])
    elif lang == "java":
        Parser(lang, formal_structures, "Language/Java/Java_Parser.py",
               "Language/Java/Java_Parser.py")
        # os.system("python Language/Python/Python_Parser_new.py "+sys.argv[2])
    else:
        print("Parser not found")


if __name__ == "__main__":
    ext = sys.argv[2].split(".")[-1]
    with open(sys.argv[1], encoding='utf-8') as f:
        formal_structure = f.readlines()
    factory(ext, formal_structure)
