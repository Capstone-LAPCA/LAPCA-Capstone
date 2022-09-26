import sys
import os
from makeParser import Parser


class MainModule:
    def __init__(self, formal_structures, test_file):
        self.formal_structures = formal_structures
        self.test_file = test_file
        self.lang = self.getLang()

    def factory(self):
        open("Language/Python/Python_Parser_new.py", "w").close()
        if self.lang == "py":
            Parser(self.lang, self.formal_structures, "Language/Python/Python_Parser.py",
                "Language/Python/Python_Parser_new.py")
            os.system("python3 Language/Python/Python_Parser_new.py "+self.test_file + " | tee results.txt")
        elif self.lang == "c":
            Parser(self.lang, self.formal_structures, "Language/C/C_Parser.py",
                "Language/C/C_Parser_new.py")
            os.system("python3 Language/C/C_Parser_new.py "+self.test_file+ " | tee results.txt")
        elif self.lang == "java":
            Parser(self.lang, self.formal_structures, "Language/Java/Java_Parser.py",
                "Language/Java/Java_Parser_new.py")
            os.system("python3 Language/Java/Java_Parser_new.py "+self.test_file+ " | tee results.txt")
        
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

    def run(self):
        self.factory()
    

if __name__ == "__main__":
    formal_structures = sys.argv[1]
    test_file = sys.argv[2]
    Module = MainModule(formal_structures, test_file)
    Module.run()
    # ext = sys.argv[2].split(".")[-1]
    # with open(sys.argv[1], encoding='utf-8') as f:
    #     formal_structure = f.readlines()
    # factory(ext, formal_structure,sys.argv[2])
