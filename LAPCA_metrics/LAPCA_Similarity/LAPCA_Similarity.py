from LAPCA_Plag import LAPCA_Plag
import os
import zipfile


class LAPCA_Similarity:
    def __init__(self, input_file, output_file, lang):
        self.plagiarism = []
        self.input_file = input_file
        self.output_file = output_file


    def extractZip(self):
        print(self.input_file)
        with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
            zip_ref.extractall(self.output_file)

    def getLAPCASimilarity(self, file1, file2):
        all_fils_list = {}
        for root, dirs, files in os.walk(self.output_file):
            for file in files:
                if file.endswith(".py"):
                    all_fils_list[os.path.join(root, file)] = file
        for i in all_fils_list.keys():
            plag = []
            plag.append(all_fils_list[i])
            max_plag_file = ""
            max_plag = 0
            for j in all_fils_list.keys():
                if i!=j:
                    perc=1 #logic for plagiarism goes here
                    if perc > max_plag:
                        max_plag = perc
                        max_plag_file = all_fils_list[j]
            plag.append(max_plag_file)
            plag.append(max_plag)
            self.plagiarism.append(plag)