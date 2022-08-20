import re
rules = []
with open('Python_Grammar.lark', encoding = 'utf-8') as f:
    python_grammar = f.readlines()
    count = 0
    for i in python_grammar:
        if re.match(r"(\?)?[A-Za-z_0-9]+:",i):
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
    print(count)
