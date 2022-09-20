def test(i):
    while(i != 0):
        if(i == 0):
            return 0
        else:
            continue
    for i in range(1,10):
        continue
    return i + test(i - 1)    
