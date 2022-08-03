import sys
from sly import Parser
from Language.Python.Python_MakeParser import Python_MakeParser
from Language.C.C_MakeParser import C_MakeParser


def Factory(lang, formalStructures):
    if lang == "C":
        Parser = C_MakeParser(formalStructures)
    elif lang == "Python":
        Parser = Python_MakeParser(formalStructures)
    else:
        print("Parser not found")


if __name__ == "__main__":
    f = open(sys.argv[2], "r")
    file = f.readlines()
    Factory(sys.argv[1], file)
