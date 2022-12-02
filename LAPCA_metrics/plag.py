import pycode_similar
#import LAPCA_Score

s1 = """
def foo(a):
    if a > 1:
        return True
    return False
        """

s2 = """
class A(object):
    def __init__(self, a):
        self._a = a

    def bar(self):
        if self._a > 2:
            return True
        return False
        """

s3="""

a=10
if a > 1:
    return True
return False

        """

result1=pycode_similar.detect([s1,s2])
result2=pycode_similar.detect([s1,s3])
print(result1[0][1][0].plagiarism_percent)
print(result2[0][1][0].plagiarism_percent)
