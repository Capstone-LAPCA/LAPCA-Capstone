import re

rules = []
with open('./Language/Python/Python_Grammar.lark', encoding = 'utf-8') as f:
    python_grammar = f.readlines()
    count = 0
    for i in python_grammar:
        if re.match(r"([\?|\!])?[A-Za-z_0-9]+:",i):
            s = i.strip().split(":")[0]
            if '?' in s:
                s = s[1:]
            if '_' == s[0]:
                s = s[1:]
            flag = False
            
            for i in s:
                
                if i=='_' or i.islower():
                    continue
                else:
                    flag = True
                    break
            
            if flag:
                continue
            count+=1
            rules.append(s)
    
with open('./Language/Python/Python_Parser.py', encoding = 'utf-8') as f:    
    python_parser = f.readlines()
    x = 0
    string = "class MyTransformer(Transformer):"
    i = 0
    while(i < len(python_parser)):
        if string in python_parser[i]:
            x = i
            break
        i += 1
    

    for func in rules:
        funcname = "    def "+func+"(self, items):\n\n        pass\n"      
        python_parser.insert(x+1,"".join(funcname))
        x += 2
    
    python_parser.insert(x+1,"".join("MainTransformer().run()"))
    
    #print(python_parser)
    with open("Language/Python/Python_Parser.py", "w") as f:
            f.write("".join(python_parser))
