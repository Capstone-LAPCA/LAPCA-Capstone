import os
guidelines = []
for file in os.listdir(os.path.join("Guidelines")):
    guidelines.append(file)

for i in guidelines:
    print("Testing " + i+" for C:")
    os.system("python3 run.py ./Test_FIles/C_Test_Files/allChecks.c ./Guidelines/"+i)
    print("\nTesting " + i+" for Python:")
    os.system("python3 run.py ./Test_FIles/Python_Test_Files/allChecks.py ./Guidelines/"+i)
    print("\nTesting " + i+" for Java:")
    os.system("python3 run.py ./Test_FIles/Java_Test_Files/Test_allchecks.java ./Guidelines/"+i)
    print("--------------------------------------------------------------------------------------")
