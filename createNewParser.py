import json
import os

class createNewParser:
    def __init__(self, lang, guidelines, base_parser_path, new_parser_path):
        self.lang = lang
        self.mapping = json.load(open(os.path.abspath("./JSON/mapping.json")))
        self.guidelines = guidelines
        self.new_parser_path = new_parser_path
        with open(base_parser_path, encoding='utf-8') as f:
            self.file_lines = f.readlines()
            with open(self.new_parser_path, "w") as f:
                f.write("".join(self.file_lines))

    def createNewParser(self) -> bool:
        if self.guidelines[0][0:8]=='LANGUAGE' and self.lang not in self.guidelines[0][9:].strip().split(','):
            return "State is not applicable for the given language. Please check the State entered"
        i = 0
        while(i < len(self.guidelines)):
            code = []
            words = self.guidelines[i]
            if(words[0:5] != "STATE"):
                i += 1
                continue
            cur_state = words[6:-1]
            i+=1

            if cur_state not in self.mapping[self.lang].keys():
                return "State is not applicable for the given language. Please check the State entered"
            cur_state = self.mapping[self.lang][cur_state]
            flag=False
            while(i < len(self.guidelines)):
                words = self.guidelines[i]
                if("END_STATE" in words):
                    self.writeFileAt(cur_state, code)
                    flag=True
                    break
                else:
                    if(words[0:4]!="\t" and words[0:4]!="    " and words!="\n"):
                        return "Guideline is not indented as per LAPCA standards"
                    code.append("    "+words)
                i += 1
            if not flag:
                return "END_STATE not found for the given state"
        return ""

    def writeFileAt(self, atstate, string):
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
                if funcname in self.file_lines[i]:
                    while self.file_lines[i] != "        pass\n":
                        i += 1
                    x = i
                    break
            self.file_lines.insert(x, "".join(string))

        with open(self.new_parser_path, "w") as f:
            f.write("".join(self.file_lines))
