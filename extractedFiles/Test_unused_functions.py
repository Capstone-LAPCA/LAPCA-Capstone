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
