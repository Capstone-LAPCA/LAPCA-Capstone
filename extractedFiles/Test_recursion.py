def recursive(i):
    if i == 0:
        return 0
    else:
        return i + recursive(i - 1)

print(recursive(5))

