import re

rules = []
with open('./Python_Grammar.lark', encoding = 'utf-8') as f:
    python_grammar = f.readlines()
    count = 0
    for i in python_grammar:
        if re.match(r"([\?|\!])?[A-Za-z_0-9]+(\s)?:",i):
            s = i.strip().split(":")[0]
            if '?' in s:
                s = s[1:]
            if '_' == s[0]:
                s = s[1:]
            if '!' == s[0]:
                s = s[1:]
            flag = False
            print(s)
            for i in s:
                if i=='_':
                    continue
                elif i.islower():
                    flag = True
                    break
            if not flag:
                continue
            count+=1
            rules.append(s)

with open('Python_Parser.py', encoding = 'utf-8') as f:    
    python_parser = f.readlines()
    x = 0
    string = "class MyTransformer(visitors.Visitor):"
    i = 0
    while(i < len(python_parser)):
        if string in python_parser[i]:
            x = i
            break
        i += 1

    for func in rules:
        funcname = "    def "+func.strip(' ')+"(self, items):\n\n        pass\n"      
        python_parser.insert(x+1,"".join(funcname))
        x += 2
    
    python_parser.insert(x+1,"".join("MainTransformer().run()"))
    with open("Python_Parser.py", "w") as f:
            f.write("".join(python_parser))
