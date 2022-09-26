#Flask server for LAPCA
from flask import request, jsonify
from flask import Flask
import os
from main import MainModule
app = Flask(__name__)
mapping = {}
mapping['Dead code'] = './Guidelines/Dead_Code.lapx'
mapping['Assign in loop'] = './Guidelines/Assign_in_loop.lapx'

@app.route('/getResults', methods=['POST'])
def getResults():
    data = request.get_json()
    print(data)
    language = data['language']
    code = data['code']
    form = data['form']
    res = ""
    if language == 'Python':
        with open("test.py", "w") as text_file:
            text_file.write(code)
        for guideline in form.keys():
            if form[guideline] == True:
                MainModule(mapping[guideline], "test.py")
                with open("results.txt", "r") as text_file:
                    res+= text_file.read()
                    print(res)
                os.remove("results.txt")
                    
    elif language == 'C':
        with open("test.c", "w") as text_file:
            text_file.write(code)
        for guideline in form.keys():
            if form[guideline] == True:
                MainModule(mapping[guideline], "test.c")
                with open("results.txt", "r") as text_file:
                    res+= text_file.read()
                    print(res)
                os.remove("results.txt")
    elif language == 'Java':
        with open("test.java", "w") as text_file:
            text_file.write(code)
        for guideline in form.keys():
            if form[guideline] == True:
                MainModule(mapping[guideline], "test.java")
                with open("results.txt", "r") as text_file:
                    res+= text_file.read()
                    print(res)
                os.remove("results.txt")
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=3003)