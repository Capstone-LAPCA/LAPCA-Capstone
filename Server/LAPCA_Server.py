#Flask server for LAPCA
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
    with open(file, "w") as text_file:
        text_file.write(code)
    for guideline in form.keys():
        if form[guideline] :
            MainModule(mapping[guideline], file).factory()
            with open("results.txt", "r") as text_file:
                res+= text_file.read()

@app.route('/getResults', methods=['POST'])
def getResults():
    data = request.get_json()
    language = data['language']
    code = data['code']
    form = data['form']
    res = ""
    if language == 'Python':
        accessRes("Server/test.py",code,form,res)
    elif language == 'C':
        accessRes("Server/test.c",code,form,res)
    elif language == 'Java':
        accessRes("Server/test.java",code,form,res)
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=3003)