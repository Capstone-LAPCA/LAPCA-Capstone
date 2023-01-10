import sys
import os
from createNewParser import createNewParser as Parser
import subprocess
from pathlib import Path
from Language.Python.Python_Parser import MainTransformer as PythonTransformer
from Language.C.C_Parser import MainTransformer as CTransformer
from Language.Java.Java_Parser import MainTransformer as JavaTransformer
class MainModule:
    def __init__(self, test_file, formal_struct):
        self.formal_struct = formal_struct
        with open(self.formal_struct, encoding='utf-8') as f:
            self.guidelines = f.readlines()
        self.test_file = test_file
        self.lang = test_file.split(".")[-1]

    def run(self):
        flag, map_state_to_code = Parser(self.lang, self.guidelines).createNewParser()
        if flag!="":
            with open("results.txt", "w") as f:
                print(Path(self.formal_struct).stem,":",flag)
                f.write(flag+" \n")
        else:
            if self.lang == "py":
                PythonTransformer(map_state_to_code, self.test_file).run()
            elif self.lang == "c":
                CTransformer(map_state_to_code, self.test_file).run()
            elif self.lang == "java":
                JavaTransformer(map_state_to_code, self.test_file).run()
                
    def factory(self):
        if self.lang in ["py", "c", "java"]:
            self.run()
        else:
            print("Language not supported")
    
if __name__ == "__main__":
    MainModule(sys.argv[1], sys.argv[2]).factory()