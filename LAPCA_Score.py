import zipfile
import os
import json
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

with zipfile.ZipFile('./zipFile.zip', 'r') as zip_ref:
    zip_ref.extractall('./ExtractedFiles')

mapping = json.load(open(os.path.abspath("./JSON/guidelines.json")))["guidelines"]

max_score = 0
guidelines = []

LAPCA_score = 0
LAPCA_percent = 0

for i in mapping:
    guidelines.append([i["id"],i["label"],i["priority"]])
    max_score+=i["priority"]

no_of_files = 0
print("------------------------------------------------------------------------------------------------------------------")
for root, dirs, files in os.walk("./ExtractedFiles"):
    for file in files:
        if file.endswith(".py") or file.endswith(".c") or file.endswith(".java"):
            score = 0
            print("\t\t\tRunning LAPCA on file:", file)
            for guideline in guidelines:
                if(guidelines[2]):
                    print("-------------")
                    print(guideline[1])
                    MainModule(os.path.join(root, file), os.path.join('./Guidelines',guideline[0]) ).factory()
                    with open("results.txt", "r") as f:
                        lines = f.read().split("\n")
                        if lines[0] == 'State is not applicable for the given language. Please check the State entered ':
                            score+=guideline[2]
                            continue
                        elif lines[0].split(' ')[0]=="Traceback":
                            print(f"{bcolors.FAIL}Error in file",file)
                            print(f"{bcolors.FAIL}Terminating LAPCA Score Benchmark{bcolors.ENDC}")
                            exit(0)
                        else:
                            score += guideline[2]/len(lines)
            LAPCA_score+=score
            LAPCA_percent += (score/max_score)
            no_of_files+=1
            print(f"{bcolors.OKGREEN}LAPCA Percent for file",file,"is",score/max_score,f"{bcolors.ENDC}")
            print(f"{bcolors.OKGREEN}LAPCA Score for file",file,"is",score,f"{bcolors.ENDC}")
            print("Current avg LAPCA Score:", LAPCA_score/no_of_files)
                        
            print("------------------------------------------------------------------------------------------------------------------")

print(f"{bcolors.OKGREEN}LAPCA Score for the given codebase is",LAPCA_score/([no_of_files if no_of_files else 1][0]),bcolors.ENDC)
print(f"{bcolors.OKGREEN}LAPCA Percent for the given codebase is",LAPCA_percent/([no_of_files if no_of_files else 1][0]),bcolors.ENDC)