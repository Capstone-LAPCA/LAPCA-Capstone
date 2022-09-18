import json
from typing import Mapping


class Parser:
    def __init__(self, lang, formal_structures, base_parser_path, new_parser_path):
        self.lang = lang
        self.f = open("./JSON/mapping.json")
        self.mapping = json.load(self.f)
        self.formal_structures = formal_structures
        self.new_parser_path = new_parser_path
        with open(base_parser_path, encoding='utf-8') as f:
            self.file_lines = f.readlines()
        self.make_parser()

    def make_parser(self):
        i = 0
        code = []
        cur_state = ""
        #print(self.formal_structures)
        while(i < len(self.formal_structures)):
            words = self.formal_structures[i]
            if(words[0:5] != "STATE"):
                i += 1
                continue
            cur_state = words[6:-1]
            i+=1
            cur_state = self.mapping[self.lang][cur_state]
            while(i < len(self.formal_structures)):
                words = self.formal_structures[i]
                if("END_STATE" in words):
                    self.write_file_at(cur_state, code)
                    break
                else:
                    code.append("    "+words)
                i += 1
            code = []

    def write_file_at(self, atstate, string):
        if atstate == "before":
            string = [i.strip()+'\n' for i in string]
            self.file_lines = string + self.file_lines
        elif atstate == "after":
            for i in range(len(self.file_lines)):
                if "return\n" in self.file_lines[i]:
                    self.file_lines = self.file_lines[:i] + string + self.file_lines[i:]
                    break
        else:
            funcname = "def "+atstate+"(self, items):"
            x = 0
            for i in range(len(self.file_lines)):
                # print(self.file_lines[i])
                if funcname in self.file_lines[i]:
                    while self.file_lines[i] != "        pass\n":
                        i += 1
                    x = i-1
                    break
            if x == 0:
                print("improper Formal structure,check state name")
                return
            self.file_lines.insert(x+1, "".join(string))

        with open(self.new_parser_path, "w") as f:
            f.write("".join(self.file_lines))
