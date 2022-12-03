import pygments.token
import pygments.lexers

class LAPCA_Clean:
    def __init__(self,lang):
        self.lang = lang
        pass
    def tokenize(self,text):

        lexer = pygments.lexers.guess_lexer_for_filename("test."+self.lang, text)
        tokens = list(lexer.get_tokens(text))
        result = []
        count1 = 0
        count2 = 0
        for i in range(len(tokens)):
            if tokens[i][0] == pygments.token.Name and not i == len(tokens) - 1 and not tokens[i + 1][1] == '(':
                result.append(('N', count1, count2))  #all variable names as 'N'
                count2 += 1
            elif tokens[i][0] in pygments.token.Literal.String:
                result.append(('S', count1, count2))  #all strings as 'S'
                count2 += 1
            elif tokens[i][0] in pygments.token.Name.Function:
                result.append(('F', count1, count2))   #user defined function names as 'F'
                count2 += 1
            elif tokens[i][0] in pygments.token.Comment.Preproc or tokens[i][0] in pygments.token.Comment.PreprocFile:
                result.append((tokens[i][1], count1, count2))
                count2 += len(tokens[i][1])
            elif tokens[i][0] in pygments.token.Text or tokens[i][0] in pygments.token.Comment or tokens[i][1]=='{' or tokens[i][1]=='}':
                pass   #whitespaces and comments ignored
            else:
                result.append((tokens[i][1], count1, count2))
                #tuples in result-(each element e.g 'def', its position in original code file, position in cleaned up code/text) 
                count2 += len(tokens[i][1])
            count1 += len(tokens[i][1])
        return result

    def toText(self,arr):
        cleanText = ''.join(str(x[0]) for x in arr)
        return cleanText
    
    def Clean(self,code):
        token = self.tokenize(code)
        text = self.toText(token)
        return text

if __name__ == '__main__':
    lc = LAPCA_Clean()
    print(lc.toText(lc.tokenize('tests/test2.py')))
