class Parser:
    def __init__(self, lang, formal_structures, base_parser_path, new_parser_path):
        self.lang = lang
        self.mapping = {}
        self.mapping['c'] = {}
        self.mapping['c']['declr'] = "assignmentexpression"
        self.mapping['py'] = {}
        self.mapping['py']['declr'] = "assign"

        self.formal_structures = formal_structures
        self.new_parser_path = new_parser_path
        with open(base_parser_path, encoding='utf-8') as f:
            self.file_lines = f.readlines()
        self.make_parser()

    def make_parser(self):
        i = 0
        code = []
        cur_state = ""
        while(i < len(self.formal_structures)):
            # print(self.formal_structures[i])
            words = self.formal_structures[i]
            if(not words):
                continue
            if(words[0:5] != "STATE"):
                i += 1
                break
            i += 1
            cur_state = words[6:-1]
            cur_state = self.mapping[self.lang][cur_state]
            while(i < len(self.formal_structures)):
                words = self.formal_structures[i]
                if(words == "END_STATE\n"):
                    break
                else:
                    code.append("    "+words)
                i += 1
        print(cur_state)
        self.write_file_at(cur_state, code)

    def write_file_at(self, atstate, string):
        funcname = "def "+atstate+"(self, items):"
        x = 0
        print(funcname)
        for i in range(len(self.file_lines)):
            # print(self.file_lines[i])
            if funcname in self.file_lines[i]:
                x = i
                break
        if x == 0:
            print("improper Formal structure,check state name")
            return
        self.file_lines.insert(x+1, "".join(string[:-1]))

        with open(self.new_parser_path, "w") as f:
            f.write("".join(self.file_lines))
