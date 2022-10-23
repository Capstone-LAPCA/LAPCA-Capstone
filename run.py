from main import MainModule
import sys
import subprocess

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

def compilePhase(lang):
    if lang=="c":
        return runCommand(["gcc","-c",test_file])
    elif lang=="java":
        return runCommand(["javac",test_file])
    elif lang=="py":
        return runCommand([sys.executable,"-m","py_compile",test_file])

test_file = sys.argv[1]
lang = test_file.split(".")[-1]
formal_struct = sys.argv[2:]

if not compilePhase(lang):
    for i in formal_struct:
        MainModule(test_file,i).factory()