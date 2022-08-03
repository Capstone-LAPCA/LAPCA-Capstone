import sys
from sly import Parser
from Language.Python.PythonMakeParser import PythonMakeParser
from Language.C.CMakeParser import CMakeParser


def factory(lang, formal_structures):
    if lang == "C":
        parser = CMakeParser(formal_structures)
    elif lang == "Python":
        parser = PythonMakeParser(formal_structures)
    else:
        print("Parser not found")


if __name__ == "__main__":
    with open(sys.argv[2], "r") as f:
        file = f.read().splitlines()
        factory(sys.argv[1], file)
