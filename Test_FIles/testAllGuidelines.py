import os
import sys
import subprocess
guidelines = []
for file in os.listdir(os.path.join("Guidelines")):
    guidelines.append(file)

for i in guidelines:
    print("Testing " + i+" for C:")
    os.system("python3 main.py ./Guidelines/"+i+" ./Test_FIles/C_Test_Files/allChecks.c")
    print("\nTesting " + i+" for Python:")
    os.system("python3 main.py ./Guidelines/"+i+" ./Test_FIles/Python_Test_Files/allChecks.py")
    print("\nTesting " + i+" for Java:")
    os.system("python3 main.py ./Guidelines/"+i+" ./Test_FIles/Java_Test_Files/Test_allchecks.java")
    print("--------------------------------------------------------------------------------------")
