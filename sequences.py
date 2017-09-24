# Generates fibonacci sequence up to a given length
def fibonacci(length):
    fib = [1, 1]

    while len(fib) < length:
        fib.append(fib[-1] + fib[-2])

    return fib
