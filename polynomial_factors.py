import parser
import tokenize
from io import StringIO
from math import sqrt

from polynomial_base import *


def get_divisors(n):
    divisors = set()
    for i in range(1, int(sqrt(abs(n)) + 1)):
        if n % i == 0:
            divisors.update([i, n // i])  # Positive divisors

    divisors.update([-x for x in divisors])  # Negative divisors

    return divisors


def get_real_roots(_eq):
    terms = [token[1] for token in tokenize.generate_tokens(StringIO(_eq).readline) if token[1]]  # Better eq.split()

    try:
        final_term = int("".join(terms[-2:]))  # Constant
    except ValueError:
        print("Invalid expression:", _eq, ", final term must be an integer constant")
        return "Error"

    _eq = parser.compilest(parser.expr(_eq))  # Parses string expression into executable code
    possible_roots = get_divisors(final_term)
    _roots = [x for x in possible_roots if eval(_eq) == 0]

    return _roots


def divide_poly(equation, divisor):
    pass


# Expressions to be factored
# Must be in terms of x only. Must use python expression syntax. No brackets.
# Must end with a constant. All coefficients must be integers.
equations = ["x ** 3 - 2 * x ** 2 - 29 * x + 30",
             "x ** 4 - 3 * x ** 3 + 6 * x ** 2 - 12 * x + 8",
             "x ** 3 - 2 * x ** 2 + 2 * x - 4",
             "x ** 2 + 4 * x + 4"]

for e in equations:
    print(e, "Roots:", get_real_roots(e), sep="\t")
    print()

t1 = Term(1, 2)
t2 = Term(5, -3)
t3 = Term(6, 2)
x3 = t1 * t2
x4 = t1 + t3

print(t1, "*", t2, "=", x3)
print(t1, "+", t3, "=", x4)

f1 = Fraction(1, 3)
f2 = Fraction(2, 5)
g1 = f1 + f2
g2 = f1 - f2
g3 = f1 * f2
g4 = f1 / f2

print(f1, "+", f2, "=", g1)
print(f1, "-", f2, "=", g2)
print(f1, "*", f2, "=", g3)
print(f1, "/", f2, "=", g4)

ft1 = Term(Fraction(1, 3), Fraction(4, 5))
ft2 = Term(Fraction(5, 7), Fraction(4, 5))
print("ft1:", ft1)
print("ft2:", ft2)

gt1 = ft1 + ft2
gt2 = ft1 * ft2
gt3 = ft1 - ft2
gt4 = ft1 / ft2
print(ft1, "+", ft2, "=", gt1)
print(ft1, "*", ft2, "=", gt2)
print(ft1, "-", ft2, "=", gt3)
print(ft1, "/", ft2, "=", gt4)
