import sys
import os
from makeParser import Parser
import subprocess


class MainModule:
    def __init__(self, formal_struct, test_file):
        with open(formal_struct, encoding='utf-8') as f:
            self.formal_structures = f.readlines()
        self.test_file = test_file
        self.lang = test_file.split(".")[-1]

    def run(self,base_parser_path, new_parser_path):
        flag = Parser(self.lang, self.formal_structures, base_parser_path,
                new_parser_path).make_parser()
        if not flag:
            with open("results.txt", "w") as f:
                print("Invalid Guideline for the given language. Please check the guideline selected")
                f.write("Invalid Guideline for the given language. Please check the guideline selected\n")
        else:
            with subprocess.Popen([sys.executable, new_parser_path, self.test_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True) as p, open("results.txt", "w") as f:
                for line in p.stdout: 
                    print(line, end='') 
                    f.write(line)
                
    def factory(self):
        if self.lang == "py":
            self.run(os.path.abspath("Language/Python/Python_Parser.py"),os.path.abspath("Language/Python/Python_Parser_new.py"))
        elif self.lang == "c":
            self.run(os.path.abspath("Language/C/C_Parser.py"),os.path.abspath("Language/C/C_Parser_new.py"))
        elif self.lang == "java":
            self.run(os.path.abspath("Language/Java/Java_Parser.py"),os.path.abspath("Language/Java/Java_Parser_new.py"))
        else:
            print("Language not supported")
    
if __name__ == "__main__":
    MainModule(sys.argv[1], sys.argv[2]).factory()