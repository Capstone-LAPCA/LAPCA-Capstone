#Flask server for LAPCA
from flask import request, jsonify, Flask
from flask_cors import CORS, cross_origin
import sys
import os
import subprocess
import json
import base64
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from main import MainModule
from LAPCA_metrics.LAPCA_Score import LAPCA_Score
from Server.Mail import Mail

# from LAPCA_metrics.LAPCA_Similarity import LAPCA_Similarity

if(os.getcwd().split(os.sep)[-1]=='Server'):
    os.chdir('..')
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
    for guideline in form:
        if guideline["checked"]:
            temp = {}
            MainModule(file,os.path.join("Guidelines",guideline["id"])).factory()
            for i in guideline_mapping:
                if i["id"] == guideline["id"]:
                    temp["name"] = i["label"]
            with open("results.txt", "r") as text_file:
                s=text_file.read()
                temp["remark"] = s
                comp_result["guidelines"].append(temp)
    return comp_result    

def userDefAccessRes(file,form,comp_result):
    s = ""
    for guideline in form:
        if guideline["checked"]:
            temp = {}
            temp["name"] = guideline["label"]
            file_name = "".join(guideline["label"].split(" "))+".lapx"
            with open(os.path.join("Guidelines","UserDefGuidelines",file_name),"w") as f:
                f.write(guideline["code"])
            MainModule(file,os.path.join("Guidelines","UserDefGuidelines",file_name)).factory()
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
    guidelines [
        {
            label: "Guideline Name",
            remark: "Compilation Error",
        },
        ...
    ]
}
'''

"""
{
    "language": "c",
    "code":"sdafasd",
    'formpredef':{
        "variable_var":true,
        "check":false
    }
"CustomGuideline":[0:{
"checked": True,
"label":"check yada yada",
"guideline":"State vsvmvof EndState"
},
1:{
"checked": false
"label":"check yada boda"
"guideline":"State vsvmvof EndState"
},
2:{
"checked": True,
"label":"check yada sada",
"guideline":"State vsvmvof EndState"
}]
}

"""

@app.route('/getResults', methods=['POST'])
@cross_origin()
def getResults():
    data = request.get_json()
    language = data['language']
    code = data['code']
    form = data['predefined_guidelines']
    user_defined_guidelines = data['custom_guidelines']
    print(form)
    file_path=os.path.join("Server","test."+language)
    res = ""
    comp_result = {
        "compilationErr":False,
        "compilationOutput": "",
        "guidelines": [], 
        "score": 552
    }

    with open(file_path, "w") as text_file:
        text_file.write(code)

    if not compilePhase(language,file_path):
        comp_result["compilationErr"]=False
        comp_result["compilationOutput"]="Compilation Successful"
        comp_result=accessRes(file_path,form,comp_result)
        comp_result=userDefAccessRes(file_path,user_defined_guidelines,comp_result)
    else:
        with open("results.txt", "r") as text_file:
            res=text_file.read()
            comp_result["compilationErr"] = True
            comp_result["compilationOutput"] = res

    return jsonify(comp_result)

@app.route('/getGuidelines', methods=['GET'])
@cross_origin()
def getGuidelines():
    json_file = json.load(open(os.path.abspath("./JSON/guidelines.json")))
    # json_file = json.load(open(r"C:\Users\Hp\Documents\LAPCA-Capstone\JSON\guidelines.json"))

    for i in range(len(json_file["guidelines"])):
        id = json_file["guidelines"][i]["id"]
        if os.path.isfile(os.path.join("Guidelines",id)):
            with open(os.path.join("Guidelines",id), "r") as text_file:
                s=text_file.read()
                json_file["guidelines"][i]["lapx_code"]=s
        else:
            return jsonify({"error":"Guideline file not found"})
    return jsonify(json_file)

@app.route("/upload_file", methods=['POST'])
@cross_origin()
def uploadFile():
    data = request.get_json()
    zipfile = data['uploadFile']['data']
    with open("temp.zip", "wb") as f:
        f.write(base64.b64decode(zipfile))
    LAPCA_Score(os.path.abspath("temp.zip"),os.path.abspath("extractedFiles")).getLAPCA_Score()
    Mail(data['name'],data['email'],data['reportType']).sendMail()
    return jsonify({'data':"success"})

if __name__ == '__main__':
    app.run(port=3003)