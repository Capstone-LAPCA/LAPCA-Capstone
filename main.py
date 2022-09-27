import sys
import os
from makeParser import Parser


class MainModule:
    def __init__(self, formal_struct, test_file):
        with open(formal_struct, encoding='utf-8') as f:
            self.formal_structures = f.readlines()
        self.test_file = test_file
        self.lang = self.getLang()

    def factory(self):
        open("Language/Python/Python_Parser_new.py", "w").close()
        if self.lang == "py":
            s = Parser(self.lang, self.formal_structures, "Language/Python/Python_Parser.py",
                "Language/Python/Python_Parser_new.py").make_parser()
            if s == 0:
                with open("results.txt", "w") as f:
                    f.write("Invalid Guideline for the given language. Please check the guideline selected\n")
                return
            os.system("python3 Language/Python/Python_Parser_new.py "+self.test_file + " 2>&1 | tee results.txt")
        elif self.lang == "c":
            s = Parser(self.lang, self.formal_structures, "Language/C/C_Parser.py",
                "Language/C/C_Parser_new.py").make_parser()
            if s == 0:
                with open("results.txt", "w") as f:
                    f.write("Invalid Guideline for the given language. Please check the guideline selected\n")
                return
            os.system("python3 Language/C/C_Parser_new.py "+self.test_file+ " 2>&1 | tee results.txt")
        elif self.lang == "java":
            s = Parser(self.lang, self.formal_structures, "Language/Java/Java_Parser.py",
                "Language/Java/Java_Parser_new.py").make_parser()
            if s == 0:
                with open("results.txt", "w") as f:
                    f.write("Invalid Guideline for the given language. Please check the guideline selected\n")
                return
            os.system("python3 Language/Java/Java_Parser_new.py "+self.test_file+ " 2>&1 | tee results.txt")
        else:
            print("Parser not found")

    def getLang(self):
        if self.test_file.endswith(".py"):
            return "py"
        elif self.test_file.endswith(".c"):
            return "c"
        elif self.test_file.endswith(".java"):
            return "java"
        else:
            print("Language not supported")
            sys.exit(0)
    
if __name__ == "__main__":
    test_file = sys.argv[2]
    Module = MainModule(sys.argv[1], test_file)
    Module.factory()