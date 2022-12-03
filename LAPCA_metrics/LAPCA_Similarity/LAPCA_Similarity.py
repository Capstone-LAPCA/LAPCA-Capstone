import os
from LAPCA_metrics.LAPCA_Similarity.LAPCA_Plag import LAPCA_Plag
import zipfile


class LAPCA_Similarity:
    def __init__(self, input_file, output_file):
        self.plagiarism = []
        self.input_file = input_file
        self.output_file = output_file


    def extractZip(self):
        with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
            zip_ref.extractall(self.output_file)

    def getLAPCA_Similarity(self):
        self.extractZip()
        file_list = {}
        for root, dirs, files in os.walk(self.output_file):
            for file in files:
                if file.endswith(".py") or file.endswith(".java") or file.endswith(".c"):
                    file_list[os.path.join(root, file)] = file
        for i in file_list.keys():
            with open (i, "r") as f:
                code1 = f.read()
            plag = []
            plag.append(file_list[i])
            max_plag_file = ""
            max_plag = 0
            max_plag_code = code1
            for j in file_list.keys():
                with open (j, "r") as f:
                    code2 = f.read()
                if i!=j:
                    perc,code=LAPCA_Plag(code1,code2,"c").check_similarity() #remove c
                    if perc > max_plag:
                        max_plag = perc
                        max_plag_file = file_list[j]
                        max_plag_code = code
            plag.append(max_plag)
            plag.append(max_plag_file)
            plag.append(max_plag_code)
            self.plagiarism.append(plag)
        print(self.plagiarism)
        return self.plagiarism

if __name__ == "__main__":
    LAPCA_Similarity("LAPCA_metrics/LAPCA_Similarity/input.zip", "output").getLAPCA_Similarity()