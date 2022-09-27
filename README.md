# LAPCA

Language Agnostic Program Conformance Analysis

---

## Contributors

[Manish Reddy](https://github.com/Manish-22)  
[Nandana C](https://github.com/NandanaC)  
[Sethupathy Venkatraman](https://github.com/sethupathyrv)  
[Swaroop Bhat](https://github.com/Soupy710)

---

## Steps to Run

### Note:

- Replace "Formal-Structure-File" to actual file name
- Replace "Python\-New-Parser" to "Preferred Language\Newly generated Parser"
- Select appropriate test file

```
git clone https://github.com/Capstone-LAPCA/LAPCA-Capstone.git
cd LAPCA-CAPSTONE
pip install -r requirements.txt
python .\main.py .\Language\Python\Formal-Structure-File \Test_FIles\Python_Test_Files\Test_var_greater_31.py
```

For Python:

```
python .\main.py .\Guidelines\var_greater_than_31.lapx .\Test_Files\Python_Test_Files\Test_var_greater_31.py
python ./main.py ./Guidelines/var_greater_than_31.lapx ./Test_Files/Python_Test_Files/Test_var_greater_31.py
```

For C:

```
python .\main.py .\Guidelines\var_greater_than_31.lapx .\Test_Files\C_Test_Files\Test_var_greater_31.c
python ./main.py ./Guidelines/var_greater_than_31.lapx ./Test_Files/C_Test_Files/Test_var_greater_31.c
```

For Java:

```
python .\main.py .\Guidelines\var_greater_than_31.lapx .\Test_FIles\Java_Test_Files\Test_var_greater_31.java
python ./main.py ./Guidelines/var_greater_than_31.lapx ./Test_FIles/Java_Test_Files/Test_var_greater_31.java
```

## Start the LAPCA server by executing the below command:
```
python LAPCA_Server.py
```