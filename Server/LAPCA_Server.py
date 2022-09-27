#Flask server for LAPCA
from re import S
from flask import request, jsonify
from flask import Flask
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from main import MainModule
app = Flask(__name__)
mapping = {}
mapping['Dead code'] = './Guidelines/Dead_Code.lapx'
mapping['Assign in loop'] = './Guidelines/Assign_in_loop.lapx'


def accessRes(file,code,form,res):
    s = ""
    with open(file, "w") as text_file:
        text_file.write(code)
    for guideline in form.keys():
        if form[guideline] :
            MainModule(mapping[guideline], file).factory()
            with open("results.txt", "r") as text_file:
                s+=text_file.read()
    return s
    

@app.route('/getResults', methods=['POST'])
def getResults():
    data = request.get_json()
    language = data['language']
    code = data['code']
    form = data['form']
    res = ""
    if language == 'Python':
        res+=accessRes("Server/test.py",code,form,res)
    elif language == 'C':
        res+=accessRes("Server/test.c",code,form,res)
    elif language == 'Java':
        res+=accessRes("Server/test.java",code,form,res)
    print(res)
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=3003)