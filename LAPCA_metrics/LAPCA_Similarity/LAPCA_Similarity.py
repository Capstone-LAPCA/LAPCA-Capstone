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
        self.pdf.set_font("Arial", size = 12)
        for i in self.plagiarism:
            self.pdf.cell(200, 10, txt = i[0], ln = 1, align = 'C')
            self.pdf.set_fill_color(255, 0,0)
            self.pdf.cell(200, 10, txt = "Plagiarism Percentage: "+str(i[1])[:5]+"%", ln = 1, align = 'C')
            self.pdf.cell(200, 10, txt = "Plagiarised File: "+str(i[2]), ln = 1, align = 'C')
            self.pdf.cell(200, 10, txt = "Plagiarised Code:\n",align='L')
            self.pdf.set_font("Arial", size = 8)
            self.pdf.cell(200, 10, txt ="", ln = 1, align = 'C')
            setColor = False
            for j in i[3].split("\n"):
                li = j.split("COLOR")
                colorPresent = False
                if len(li) > 1:
                    colorPresent = True
                if li[0]=='' and len(li)>1:
                    setColor = not setColor
                for k in li:   
                    if k=="":
                        continue
                    if setColor:
                        #self.pdf.set_text_color(255, 0, 0)
                        self.pdf.set_fill_color(255, 354, 23)
                        self.pdf.cell(len(k)+8, 5, txt = k, ln = 0, align = 'L',fill=True)
                        self.pdf.set_text_color(0, 0, 0)
                    else:
                        self.pdf.cell(len(k)+8, 5, txt = k, ln = 0, align = 'L')
                    if colorPresent:
                        setColor = not setColor
                if li[len(li)-1]!="" and len(li)>1:
                    setColor = not setColor
                self.pdf.cell(200, 5, txt ="", ln = 1, align = 'C')
            self.pdf.set_font("Arial", size = 15)
        self.pdf.output("LAPCA_metrics/Similarity_Score_Pdf/resultsSimilarity.pdf",'F')
        self.mergePdf()

    def mergePdf(self):
        merger = PyPDF2.PdfFileMerger()
        f1 = os.path.abspath('LAPCA_metrics/Similarity_Score_Pdf/Report_Cover_Page.pdf')
        f2 = os.path.abspath('LAPCA_metrics/Similarity_Score_Pdf/resultsSimilarity.pdf')
        merger.append(f1)
        merger.append(f2)
        merger.write("LAPCA_metrics/Similarity_Score_Pdf/Report.pdf")

    def getLAPCA_Similarity(self):
        csv_report = open("LAPCA_metrics/Similarity_Score_Pdf/LAPCA_Similarity.csv","w")
        csv_report.write("File Name,Plagiarised File,Plagiarism Percentage\n")
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
                        if max_plag == 100:
                            break
            plag.append(max_plag)
            plag.append(max_plag_file)
            plag.append(max_plag_code)
            print(plag[0],"plagiarised",plag[2],"by",plag[1],"%")
            csv_report.write(str(plag[0])+","+plag[2]+","+str(plag[1])+"\n")
            self.plagiarism.append(plag)
        return self.plagiarism

if __name__ == "__main__":
    lc = LAPCA_Similarity("LAPCA_metrics/LAPCA_Similarity/xytest.zip", "LAPCA_metrics/LAPCA_Similarity/output1")
    lc.getLAPCA_Similarity()
    lc.createPdf()
