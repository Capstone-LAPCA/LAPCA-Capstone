#Flask server for LAPCA
from flask import request, jsonify, Flask
from flask_cors import CORS, cross_origin
import sys
import os
import subprocess
import json
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from main import MainModule
app = Flask(__name__)
CORS(app)

def runCommand(command):
    flag=False
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True) as p, open("results.txt", "w") as f:
        for line in p.stdout: 
            if(line.startswith('Picked up')): #heroku javac fix
                continue
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

def accessRes(file,form,comp_result):
    guideline_mapping = json.load(open(os.path.abspath("./JSON/guidelines.json")))
    guideline_mapping = guideline_mapping["guidelines"]
    s = ""
    for guideline in form.keys():
        if form[guideline]:
            temp = {}
            MainModule(file,os.path.join("Guidelines",guideline)).factory()
            for i in guideline_mapping:
                if i["id"] == guideline:
                    temp["name"] = i["label"]
            with open("results.txt", "r") as text_file:
                s=text_file.read()
                temp["remark"] = s
                comp_result["guidelines"].append(temp)
    return comp_result    

@app.route('/')
def home():
    return "LAPCA Server"

'''
API
Guideline    String
CompilationErr    Bool 
Remark    String
Result    Bool

structure of json:
{
    compilationErr:Bool,
    compilationOutput: "Compilation Output",
    guidelines {
        guideline1: {
            remark: "Compilation Error",
        },
        guideline2: {
            remark: "Program satisfies all the selected guidelines",
        }
    }
}
'''


@app.route('/getResults', methods=['POST'])
@cross_origin()
def getResults():
    data = request.get_json()
    language = data['language']
    code = data['code']
    form = data['form']
    file_path=os.path.join("Server","test."+language)
    res = ""
    comp_result = {
        "compilationErr":False,
        "compilationOutput": "",
        "guidelines": []
    }

    if(os.getcwd().split(os.sep)[-1]=='Server'):
        os.chdir('..')

    with open(file_path, "w") as text_file:
        text_file.write(code)

    if not compilePhase(language,file_path):
        comp_result["compilationErr"]=False
        comp_result["compilationOutput"]="Compilation Successful"
        comp_result=accessRes(file_path,form,comp_result)
    else:
        with open("results.txt", "r") as text_file:
            res=text_file.read()
            comp_result["compilationErr"] = True
            comp_result["compilationOutput"] = res

    return jsonify(comp_result)

@app.route('/getGuidelines', methods=['GET'])
@cross_origin()
def getGuidelines():
    return json.load(open(os.path.abspath("./JSON/guidelines.json")))

if __name__ == '__main__':
    app.run(port=3003)