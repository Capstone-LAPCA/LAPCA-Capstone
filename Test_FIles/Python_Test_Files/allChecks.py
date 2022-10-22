#iterative function to implement binary search
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    while low == high:
        mid = (high + low) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

print(binary_search([1,2,3,4,5,6,7,8,9,10], 5))


def test(i):
    while(i != 0):
        if(i == 0):
            return 0
        else:
            continue
    for i in range(1,10):
        continue
    return i + test(i - 1)    

def testfun(x):
    if x == 1:
        Y = 1
        return 1
        z = 5
    return 4
    x = 5
    print(x)

def recursive(i):
    if i == 0:
        return 0
    else:
        return i + recursive(i - 1)

print(recursive(5))


def sum(a,b):
    x = a + b
    product(a,b)
    return x

def product(a,b):
    x = a * b
    return x

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == "__main__":
    print(sum(5,5))


a = 5
qwdhvsdhvsivoasvpsavdsuavpasbvpabbvbnndfghjsdfghsdfghsdfghsdfgsie = 0
asdhsbfhdsg = 0