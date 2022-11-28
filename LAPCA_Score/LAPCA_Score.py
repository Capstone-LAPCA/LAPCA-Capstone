import zipfile
import os
import json
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from main import MainModule

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


class LAPCA_Score:
    def __init__(self, input_file, output_file, *args, **kwargs):
        self.input_file = input_file
        self.output_file = output_file
        self.mapping = json.load(open(os.path.abspath("./JSON/guidelines.json")))["guidelines"]
        self.result = {}
        self.max_score = 0
        self.LAPCA_score = 0
        self.LAPCA_percent = 0
        self.guidelines = []
        self.err_count = 0
        self.error_files = []
        self.violation_count = {}
        with open('LAPCA_Score/LAPCA_Score_Report.txt', 'w') as f:
            f.write("")
        for i in self.mapping:
            if i["priority"]:
                self.violation_count[i["id"]] = 0
                self.guidelines.append([i["id"],i["label"],i["priority"]])
                self.max_score+=i["priority"]

    def extractZip(self):
        with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
            zip_ref.extractall(self.output_file)
        
        
    def getLAPCA_Score(self):
        no_of_files = 0
        print("------------------------------------------------------------------------------------------------------------------")
        for root, dirs, files in os.walk("./ExtractedFiles"):
            for file in files:
                if file.endswith(".py") or file.endswith(".c") or file.endswith(".java"):
                    self.result[file] = {}
                    flag = False
                    score = 0
                    print("----------------------------------------")
                    print("\t\t\tRunning LAPCA on file:", file)
                    with open('LAPCA_Score_Report.txt', 'a+') as f:
                        f.write("------------------------------------------------------------------------------------------------------------------\n")
                        f.write("\t\t\t\t\t\t\t\t\t\tFile: "+file+"\n")
                    for guideline in self.guidelines:
                        self.result[file][guideline[1]] = []
                        MainModule(os.path.join(root, file), os.path.join('./Guidelines',guideline[0]) ).factory()
                        with open("results.txt", "r") as f:
                            lines = f.read().split("\n")
                            if lines[0] == 'State is not applicable for the given language. Please check the State entered ' or lines[0] == 'Guideline is not applicable for the given language. Please check the languages mentioned in the guideline. ':
                                score+=guideline[2]
                                continue
                            elif lines[0].split(' ')[0]=="Traceback":
                                print(f"{bcolors.FAIL}Error in file",file,f"{bcolors.ENDC}")
                                #print(f"{bcolors.FAIL}Terminating LAPCA Score Benchmark{bcolors.ENDC}")
                                #return "Error in file"+file+".\nTerminating LAPCA Score Benchmark\n"
                                #exit(0)
                                self.error_files.append(file)
                                self.err_count+=1
                                flag = True
                                break

                            else:
                                self.violation_count[guideline[0]]+=len(lines)-1
                                with open('LAPCA_Score_Report.txt', 'a+') as f:
                                    for i in lines[:-1]:
                                        f.write("\t\t\t"+i+"\n\n")
                                self.result[file][guideline[1]].extend(lines[:-1])
                                score += guideline[2]/len(lines)
                    if flag:
                        continue
                    self.LAPCA_score+=score
                    self.LAPCA_percent += (score/self.max_score)
                    no_of_files+=1
                    with open('LAPCA_Score_Report.txt', 'a+') as f:
                        f.write("\t\t\tFile Number: "+str(no_of_files)+"\n")
                        f.write("\t\t\tLAPCA Score for file "+file+" is "+str(score)+"\n")
                        f.write("\t\t\tLAPCA Percentage for file "+file+" is "+str(score/self.max_score)+"\n")
                        f.write("\t\t\tCurrent avg LAPCA Score is "+str(self.LAPCA_score/no_of_files)+"\n")
                    print(f"{bcolors.OKGREEN}Number of files processed:", no_of_files,f"{bcolors.ENDC}")
                    print(f"{bcolors.OKGREEN}LAPCA Percent for file",file,"is",score/self.max_score,f"{bcolors.ENDC}")
                    print(f"{bcolors.OKGREEN}LAPCA Score for file",file,"is",score,f"{bcolors.ENDC}")
                    print("Current avg LAPCA Score:",self.LAPCA_score/no_of_files)
                                
                    print("------------------------------------------------------------------------------------------------------------------")
        with open('LAPCA_Score_Report.txt', 'a+') as f:
            f.write("------------------------------------------------------------------------------------------------------------------\n")
            f.write("\n\n")
            f.write("\t\t\t\t\tTotal number of files processed: "+str(no_of_files)+"\n")
            f.write("\t\t\t\t\tLAPCA Score for the given codebase is "+str(self.LAPCA_score/([no_of_files if no_of_files else 1][0]))+"\n")
            f.write("\t\t\t\t\tLAPCA Percentage for the given codebase is "+str(self.LAPCA_percent/([no_of_files if no_of_files else 1][0]))+"\n")
            f.write("\t\t\t\t\tTotal number of error files: "+str(self.err_count)+"\n")
            f.write("\t\t\t\t\tError files: "+str(self.error_files)+"\n")
            f.write("\t\t\t\t\tViolation count:\n")
            for i in self.violation_count.keys():
                f.write("\t\t\t\t\t\t"+i+" : "+str(self.violation_count[i])+"\n")

            f.write("\n\n")
            f.write("------------------------------------------------------------------------------------------------------------------\n")
        print(f"{bcolors.OKGREEN}Total number of files:",no_of_files,f"{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}LAPCA Score for the given codebase is",self.LAPCA_score/([no_of_files if no_of_files else 1][0]),bcolors.ENDC)
        print(f"{bcolors.OKGREEN}LAPCA Percent for the given codebase is",self.LAPCA_percent/([no_of_files if no_of_files else 1][0]),bcolors.ENDC)

if __name__ == "__main__":
    obj = LAPCA_Score("codebase", "./ExtractedFiles")
    obj.extractZip()
    obj.getLAPCA_Score()
    print(obj.result)
    print(obj.error_files)
    print(obj.err_count)

    #node-at-a-given-index-in-linked-list.py
    #taking-input-and-typecasting-python.py