import hashlib
from LAPCA_metrics.LAPCA_Similarity.LAPCA_Clean import LAPCA_Clean

class LAPCA_Plag:
    def __init__(self, code1, code2, lang):
        self.code1 = code1
        self.lang = lang
        self.code2 = code2
        self.plagiarism_percent = 0

    def __str__(self):
        return "Similarity: " + str(self.similarity)
    
    def minIndex(self,arr):
        minI = 0
        minV = arr[0]
        n = len(arr)
        for i in range(n):
            if arr[i] < minV:
                minV = arr[i]
                minI = i
        return minI
    def get_fingerprint(self,a,size):
        prev = 0
        windows = []
        fingerprintList = []
        for i in range(len(a) - size):
            win = a[i: i + size]
            windows.append(win)
            cur = i + self.minIndex(win)
            if cur != prev:
                fingerprintList.append(a[cur]) 
                prev = cur  
        return fingerprintList

    def get_all_hash(self, list1):
        all_hash = []
        for i in list1:
            hashval = hashlib.sha1(i.encode('utf-8'))
            hashval = int(hashval.hexdigest()[-4 :],16)
            all_hash.append(hashval)
        return all_hash

    def kgrams(self, list_of_tokens, k):
        make_k_grams = [''.join(list_of_tokens[i:i+k]) for i in range(len(list_of_tokens) - k + 1)]
        make_k_hash = [self.get_all_hash([i])[0] for i in make_k_grams]
        return [(make_k_grams[i],make_k_hash[i],i,i+k) for i in range(len(make_k_grams))]

    def check_similarity(self):
        lc = LAPCA_Clean(self.lang)
        token1 = lc.tokenize(self.code1)
        token2 = lc.tokenize(self.code2)
        code1 = lc.toText(token1)
        code2 = lc.toText(token2)
        kGrams1 = self.kgrams(list(code1),10)  #stores k-grams, their hash values and positions in cleaned up text
        kGrams2 = self.kgrams(list(code2),10)
        HL1 = [i[1] for i in kGrams1] 
        HL2 = [i[1] for i in kGrams2]
        fpList1 = self.get_fingerprint(HL1,1)
        fpList2 = self.get_fingerprint(HL2,1)
        newCode = ""   #code with marked plagiarized content
        points = []
        for i in fpList1:
            for j in fpList2:
                if i == j:   
                    flag = 0
                    match = HL1.index(i)   #index of matching fingerprints in hash list, k-grams list
                    newStart = kGrams1[match][2]   #start position of matched k-gram in cleaned up code
                    newEnd = kGrams1[match][3]   #end position
                    for k in token1:
                        if k[2] == newStart:   #linking positions in cleaned up code to original code
                            startx = k[1]
                            flag = 1
                        if k[2] == newEnd:
                            flag +=1
                            endx = k[1]
                            break
                    if flag == 2:
                        points.append([startx, endx])
        # print("Plagiarism percentage: ", (count/len(fpList1))*100, "%")
        points.sort(key = lambda x: x[0])
        # print(points)
        if len(points) == 0:
            print("No plagiarism detected")
            return 0
        mergedPoints = []
        mergedPoints.append(points[0])
        for i in range(1, len(points)):
            last = mergedPoints[len(mergedPoints) - 1]
            if points[i][0] >= last[0] and points[i][0] <= last[1]: #merging overlapping regions
                if points[i][1] > last[1]:
                    mergedPoints = mergedPoints[: len(mergedPoints)-1]
                    mergedPoints.append([last[0], points[i][1]])
                else:
                    pass
            else:
                mergedPoints.append(points[i])
        newCode = self.code1[: mergedPoints[0][0]]
        plagCount = 0

        for i in range(len(mergedPoints)):
            if mergedPoints[i][1] > mergedPoints[i][0]:
                plagCount += mergedPoints[i][1] - mergedPoints[i][0]
                newCode = newCode + '\x1b[6;30;42m' + self.code1[mergedPoints[i][0] : mergedPoints[i][1]] + '\x1b[0m'
                if i < len(mergedPoints) - 1:
                    newCode = newCode + self.code1[mergedPoints[i][1] : mergedPoints[i+1][0]]
                else:
                    newCode = newCode + self.code1[mergedPoints[i][1] :]
        divi = token1[len(token1) - 1][1] - token1[0][1] - 1
        self.plagiarism_percent = (plagCount/divi)*100
        print("Approx ratio of plagiarized content in file 1: ", self.plagiarism_percent, "%")
        return self.plagiarism_percent

if "__main__" == __name__:
    code1 = open("LAPCA_metrics/test1.c", "r").read()
    code2 = open("LAPCA_metrics/test1.c", "r").read()
    LAPCA_Plag(code1, code2,"c").check_similarity()