import sys
import os
from makeParser import Parser


class MainModule:
    def __init__(self, formal_struct, test_file):
        with open(formal_struct, encoding='utf-8') as f:
            self.formal_structures = f.readlines()
        self.test_file = test_file
        self.lang = test_file.split(".")[-1]

    def run(self,base_parser_path, new_parser_path):
        s = Parser(self.lang, self.formal_structures, base_parser_path,
                new_parser_path).make_parser()
        if s == 0:
            with open("results.txt", "w") as f:
                f.write("Invalid Guideline for the given language. Please check the guideline selected\n")
            return
        os.system("python3 "+new_parser_path +" "+self.test_file + " 2>&1 | tee results.txt")
        
    def factory(self):
        if self.lang == "py":
            self.run("Language/Python/Python_Parser.py","Language/Python/Python_Parser_new.py")
        elif self.lang == "c":
            self.run("Language/C/C_Parser.py","Language/C/C_Parser_new.py")
        elif self.lang == "java":
            self.run("Language/Java/Java_Parser.py","Language/Java/Java_Parser_new.py")
        else:
            print("Language not supported")
    
if __name__ == "__main__":
    MainModule(sys.argv[1], sys.argv[2]).factory()