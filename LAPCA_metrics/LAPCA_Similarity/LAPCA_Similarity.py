import os
from LAPCA_metrics.LAPCA_Similarity.LAPCA_Plag import LAPCA_Plag
import zipfile
import PyPDF2  
from fpdf import FPDF

class LAPCA_Similarity:
    def __init__(self, input_file, output_file):
        self.plagiarism = []
        self.input_file = input_file
        self.output_file = output_file
        self.pdf = FPDF()

    def extractZip(self):
        with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
            zip_ref.extractall(self.output_file)
    
    def createPdf(self):
        self.pdf.add_page()  
        self.pdf.set_font("Arial", size = 15)
        for i in self.plagiarism:
            self.pdf.cell(200, 10, txt = i[0], ln = 1, align = 'C')
            self.pdf.cell(200, 10, txt = "Plagiarism Percentage: "+str(i[1]), ln = 1, align = 'C')
            self.pdf.cell(200, 10, txt = "Plagiarised File: "+str(i[2]), ln = 1, align = 'C')
            self.pdf.cell(200, 10, txt = "Plagiarised Code:\n",align='L')
            self.pdf.set_font("Arial", size = 8)
            for j in i[3].split("\n"):
                #REPLACE THE BELOW LOGIC
                self.pdf.cell(200, 10, txt = j, ln = 1, align = 'L')
            self.pdf.set_font("Arial", size = 15)
        #self.pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
        self.pdf.output("LAPCA_metrics/LAPCA_Score_Pdf/resultsSimilarity.pdf",'F')
        self.mergePdf()

    def mergePdf(self):
        merger = PyPDF2.PdfFileMerger()
        f1 = os.path.abspath('LAPCA_metrics/LAPCA_Score_Pdf/Report_Cover_Page.pdf')
        f2 = os.path.abspath('LAPCA_metrics/LAPCA_Score_Pdf/resultsSimilarity.pdf')
        merger.append(f1)
        merger.append(f2)
        merger.write("LAPCA_metrics/LAPCA_Score_Pdf/ReportSimilar.pdf")

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
            print(max_plag_file)
            print(max_plag)
            plag.append(max_plag)
            plag.append(max_plag_file)
            plag.append(max_plag_code)
            self.plagiarism.append(plag)
        print(self.plagiarism)
        self.createPdf()
        return self.plagiarism

if __name__ == "__main__":
    LAPCA_Similarity("LAPCA_metrics/LAPCA_Similarity/input.zip", "output").getLAPCA_Similarity()