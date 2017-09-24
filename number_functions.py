def lowest_common_multiple(a, b):
    if a + b == 0:
        return 0
    return (a * b) // greatest_common_divisor(a, b)


# Euclid's algorithm. Only works for a, b > 0
def greatest_common_divisor(a, b):
    a, b = max(a, b), min(a, b)

    while b != 0:
        r = a % b
        a = b
        b = r

    return a
