from multiprocessing.spawn import import_main_path
import sys
import os
from Language.Python.Make_Parser import PythonMakeParser
from Language.C.Make_Parser import CMakeParser
from Language.Java.Make_Parser import JavaMakeParser


def factory(ver, lang, formal_structures):
    if lang == "py":
        PythonMakeParser(formal_structures)
        os.system("python Language/Python/Python_Parser_new.py "+sys.argv[2])
    elif lang == "c":
        CMakeParser(formal_structures)
        os.system("python Language/C/C_Parser_new.py "+sys.argv[2])
    elif lang == "java":
        JavaMakeParser(formal_structures)
        # os.system("python Language/Python/Python_Parser_new.py "+sys.argv[2])
    else:
        print("Parser not found")


if __name__ == "__main__":
    ext = sys.argv[2].split(".")[-1]
    python_ver = sys.argv[-1]
    with open(sys.argv[1], encoding='utf-8') as f:
        formal_structure = f.readlines()
    factory(python_ver, ext, formal_structure)
