import zipfile
import os
import json
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from main import MainModule
import subprocess
from fpdf import FPDF
import PyPDF2

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PDF(FPDF):
    pass

def runCommand(command):
    flag=False
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True) as p, open("results.txt", "w") as f:
        for line in p.stdout: 
            print(line, end='') 
            f.write(line)
            flag=True
    return flag

def compilePhase(lang,test_file):
    if lang=="c":
        return runCommand(["gcc","-c",test_file])
    elif lang=="java":
        return runCommand(["javac",test_file])
    elif lang=="py":
        return runCommand([sys.executable,"-m","py_compile",test_file])
class LAPCA_Score:
    def __init__(self, input_file, output_file, *args, **kwargs):
        self.input_file = input_file
        self.output_file = output_file
        self.mapping = json.load(open(os.path.abspath("./JSON/guidelines.json")))["guidelines"]
        self.result = {}
        self.max_score = 0
        self.LAPCA_score = 0
        self.LAPCA_percent = 0
        self.plagiarism = []
        self.pdf = PDF()
        self.guidelines = []
        self.err_count = 0
        self.error_files = []
        self.violation_count = {}
        self.violated_file_count = {}
        with open('LAPCA_metrics/LAPCA_Score_Report.txt', 'w') as f:
            f.write("")
        for i in self.mapping:
            if i["priority"]:
                self.violation_count[i["id"]] = 0
                self.violated_file_count[i["id"]] = 0
                self.guidelines.append([i["id"],i["label"],i["priority"]])
                self.max_score+=i["priority"]
        self.extractZip()
        # self.createPdf()
        
    def createPdf(self):
        self.pdf.add_page()  
        self.pdf.set_font("Arial", size = 15)
        f = open('LAPCA_metrics/LAPCA_Score_Report.txt', "r")
        for x in f:
            self.pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
        self.pdf.output("LAPCA_metrics/LAPCA_Score_pdf/results.pdf",'F')
        self.mergePdf()

    def mergePdf(self):
        merger = PyPDF2.PdfFileMerger()
        f1 = os.path.abspath('LAPCA_metrics\LAPCA_Score_Pdf\\Report_Cover_Page.pdf')
        f2 = os.path.abspath('LAPCA_metrics\LAPCA_Score_Pdf\\results.pdf')
        merger.append(f1)
        merger.append(f2)
        merger.write("LAPCA_metrics/LAPCA_Score_pdf/Report.pdf")
    
    def sendEmail(self):
        
        pass

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

    def getLAPCA_Score(self):
        no_of_files = 0
        print("------------------------------------------------------------------------------------------------------------------")
        for root, dirs, files in os.walk(self.output_file):
            for file in files:
                if file.endswith(".py") or file.endswith(".c") or file.endswith(".java"):
                    self.result[file] = {}
                    no_of_files+=1
                    flag = False
                    score = 0
                    print("----------------------------------------")
                    print("\t\t\tRunning LAPCA on file:", file)
                    with open('LAPCA_metrics/LAPCA_Score_Report.txt', 'a+') as f:
                        f.write("------------------------------------------------------------------------------------------------------------------\n")
                        f.write("\t\t\t\t\t\t\t\t\t\tFile: "+file+"\n")
                    lang = file.split(".")[-1]
                    if compilePhase(lang,os.path.join(root, file)):
                        with open('LAPCA_metrics/LAPCA_Score_Report.txt', 'a+') as f, open('results.txt', 'r') as r:
                            f.write("Error(s) found in file: "+file+"\n")
                            f.write(r.read())
                            self.error_files.append(file)
                            self.err_count+=1
                            continue
                    for guideline in self.guidelines:
                        self.result[file][guideline[1]] = []
                        MainModule(os.path.join(root, file), os.path.join('./Guidelines',guideline[0]) ).factory()
                        with open("results.txt", "r") as f:
                            file_op = f.read()
                            lines = file_op.split("\n")
                            if lines[0] == 'State is not applicable for the given language. Please check the State entered ' or lines[0] == 'Guideline is not applicable for the given language. Please check the languages mentioned in the guideline. ':
                                score+=guideline[2]
                                continue
                            elif lines[0].split(' ')[0]=="Traceback":
                                print(f"{bcolors.FAIL}Error in file",file,f"{bcolors.ENDC}")
                                #print(f"{bcolors.FAIL}Terminating LAPCA Score Benchmark{bcolors.ENDC}")
                                #return "Error in file"+file+".\nTerminating LAPCA Score Benchmark\n"
                                #exit(0)
                                with open('LAPCA_metrics/LAPCA_Score_Report.txt', 'a+') as f:
                                    f.write("Error in file "+file+".\n")
                                    f.write(str(file_op))
                                flag = True
                                break

                            else:
                                self.violation_count[guideline[0]]+=len(lines)-1
                                if len(lines)-1 > 0:
                                    self.violated_file_count[guideline[0]]+=1
                                with open('LAPCA_metrics/LAPCA_Score_Report.txt', 'a+') as f:
                                    for i in lines[:-1]:
                                        f.write("\t\t\t"+i+"\n\n")
                                self.result[file][guideline[1]].extend(lines[:-1])
                                score += guideline[2]/len(lines)
                    if flag:
                        continue
                    self.LAPCA_score+=score
                    self.LAPCA_percent += (score/self.max_score)
                    with open('LAPCA_metrics/LAPCA_Score_Report.txt', 'a+') as f:
                        f.write("\t\t\tFile Number: "+str(no_of_files)+"\n")
                        f.write("\t\t\tLAPCA Score for file "+file+" is "+str(score)+"\n")
                        f.write("\t\t\tLAPCA Percentage for file "+file+" is "+str(score/self.max_score)+"\n")
                        f.write("\t\t\tCurrent avg LAPCA Score is "+str(self.LAPCA_score/no_of_files)+"\n")
                    print(f"{bcolors.OKGREEN}Number of files processed:", no_of_files,f"{bcolors.ENDC}")
                    print(f"{bcolors.OKGREEN}LAPCA Percent for file",file,"is",score/self.max_score,f"{bcolors.ENDC}")
                    print(f"{bcolors.OKGREEN}LAPCA Score for file",file,"is",score,f"{bcolors.ENDC}")
                    print("Current avg LAPCA Score:",self.LAPCA_score/no_of_files)
                                
                    print("------------------------------------------------------------------------------------------------------------------")
        with open('LAPCA_metrics/LAPCA_Score_Report.txt', 'a+') as f:
            f.write("------------------------------------------------------------------------------------------------------------------\n")
            f.write("\n\n")

            f.write("\t\t\t\t\tTotal number of files processed: "+str(no_of_files)+"\n")
            f.write("\t\t\t\t\tLAPCA Score for the given codebase is "+str(self.LAPCA_score/([no_of_files if no_of_files else 1][0]))+"\n")
            f.write("\t\t\t\t\tLAPCA Percentage for the given codebase is "+str(self.LAPCA_percent/([no_of_files if no_of_files else 1][0]))+"\n")

            f.write("\t\t\t\t\tTotal number of files with syntax errors: "+str(self.err_count)+"\n")
            f.write("\t\t\t\t\tFiles with syntax errors:\n")
            for i in self.error_files:
                f.write("\t\t\t\t\t\t"+i+"\n")

            f.write("\t\t\t\t\tViolation count:\n")
            for i in self.violation_count.keys():
                f.write("\t\t\t\t\t\t"+i+" : "+str(self.violation_count[i])+"\n")
            f.write("\t\t\t\t\tViolated files count:\n")
            for i in self.violated_file_count.keys():
                f.write("\t\t\t\t\t\t"+i+" : "+str(self.violated_file_count[i])+"\n")

            f.write("\n\n")
            f.write("------------------------------------------------------------------------------------------------------------------\n")
    
        print(f"{bcolors.OKGREEN}Total number of files:",no_of_files,f"{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}LAPCA Score for the given codebase is",self.LAPCA_score/([no_of_files if no_of_files else 1][0]),bcolors.ENDC)
        print(f"{bcolors.OKGREEN}LAPCA Percent for the given codebase is",self.LAPCA_percent/([no_of_files if no_of_files else 1][0]),bcolors.ENDC)
        self.createPdf()

if __name__ == "__main__":
    obj = LAPCA_Score("codebase.zip", "./ExtractedFiles")
    obj.extractZip()
    obj.getLAPCA_Score()
    # print(obj.result)
    # print(obj.error_files)
    # print(obj.err_count)
