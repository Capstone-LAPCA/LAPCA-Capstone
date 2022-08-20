with open("Language/Java/Java_Parser.py", encoding='utf-8') as f:
    file_lines = f.readlines()


class JavaMakeParser:
    def __init__(self, formal_structures):
        self.formal_structures = formal_structures
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
            while(i < len(self.formal_structures)):
                words = self.formal_structures[i]
                if(words == "END_STATE\n"):
                    break
                else:
                    code.append("    "+words)
                i += 1
        # print(code)
        self.write_file_at(cur_state, code)

    def write_file_at(self, atstate, string):
        funcname = "def "+atstate+"(self, items):"
        x = 0
        print(funcname)
        # print(file_lines)
        for i in range(len(file_lines)):
            # print(file_lines[i])
            if funcname in file_lines[i]:
                x = i
                break
        if x == 0:
            print("improper Formal structure,check state name")
            return
        file_lines.insert(x+1, "".join(string[:-1]))

        with open("Language/Java/Java_Parser_new.py", "w") as f:
            f.write("".join(file_lines))
