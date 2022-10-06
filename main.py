import sys
import os
from createNewParser import createNewParser as Parser
import subprocess
from pathlib import Path


class MainModule:
    def __init__(self, formal_struct, test_file):
        self.formal_struct = formal_struct
        with open(self.formal_struct, encoding='utf-8') as f:
            self.guidelines = f.readlines()
        self.test_file = test_file
        self.lang = test_file.split(".")[-1]

    def runCommand(self,command):
        flag=False
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True) as p, open("results.txt", "w") as f:
            for line in p.stdout: 
                if(line.startswith('Picked up')): #heroku javac fix
                    continue
                print(line, end='') 
                f.write(line)
                flag=True
        return flag

    def compilePhase(self):
        if self.lang=="c":
            return self.runCommand(["gcc",self.test_file])
        elif self.lang=="java":
            return self.runCommand(["javac",self.test_file])
        elif self.lang=="py":
            return self.runCommand([sys.executable,"-m","py_compile",self.test_file])

    def run(self,base_parser_path, new_parser_path):
        flag = Parser(self.lang, self.guidelines, base_parser_path,
                new_parser_path).createNewParser()
        if not flag:
            with open("results.txt", "w") as f:
                print(Path(self.formal_struct).stem,"not applicable for the given language. Please check the guideline selected")
                f.write(Path(self.formal_struct).stem +" not applicable for the given language. Please check the guideline selected\n")
        else:
            if self.compilePhase():
                return
            self.runCommand([sys.executable, new_parser_path, self.test_file])
                
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