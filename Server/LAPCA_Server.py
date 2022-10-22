#Flask server for LAPCA
from flask import request, jsonify, Flask
from flask_cors import CORS, cross_origin
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from main import MainModule
app = Flask(__name__)
CORS(app)

def accessRes(file,code,form):
    s = ""
    with open(file, "w") as text_file:
        text_file.write(code)
    for guideline in form.keys():
        if form[guideline] :
            MainModule(os.path.join("Guidelines",guideline),file).factory()
            with open("results.txt", "r") as text_file:
                s+=text_file.read()
    if not s:
        print('Program satisfies all the selected guidelines')
        s+='Program satisfies all the selected guidelines'
    return s    

@app.route('/')
def home():
    return "LAPCA Server"

@app.route('/getResults', methods=['POST'])
@cross_origin()
def getResults():
    data = request.get_json()
    language = data['language']
    code = data['code']
    form = data['form']
    res = ""
    if(os.getcwd().split(os.sep)[-1]=='Server'):
        os.chdir('..')
        
    if language == 'Python':
        res=accessRes(os.path.join("Server","test.py"),code,form)
    elif language == 'C':
        res=accessRes(os.path.join("Server","test.c"),code,form)
    elif language == 'Java':
        res=accessRes(os.path.join("Server","test.java"),code,form)
    return jsonify(res)

@app.route('/getGuidelines', methods=['GET'])
@cross_origin()
def getGuidelines():
    guidelines = []
    for file in os.listdir(os.path.join("Guidelines")):
        guidelines.append(file)
    return jsonify(guidelines)

if __name__ == '__main__':
    app.run(port=3003)