from functools import reduce


def lowest_common_multiple(*args):
    if len(args) == 0:
        return 0

    if len(args) == 1:
        return args[0]

    if len(args) == 2:
        a, b = args[0], args[1]
        return (a * b) // greatest_common_divisor(a, b)

    return reduce(lowest_common_multiple, args)


# Euclid's algorithm. Only works for a, b > 0
def greatest_common_divisor(*args):
    if len(args) == 0:
        return 1

    if len(args) == 1:
        return args[0]

    if len(args) == 2:
        a, b = max(args), min(args)
        while b != 0:
            a, b = b, a % b
        return abs(a)

    return reduce(greatest_common_divisor, args)
