import parser
import tokenize
from io import StringIO
from math import sqrt

from number_functions import greatest_common_divisor as gcd
from polynomial_base import Term


# TODO: gcd of Terms eg. x^4, x^3   -> x^3


def get_divisors(n):
    divisors = set()
    for i in range(1, int(sqrt(abs(n)) + 1)):
        if n % i == 0:
            divisors.update([i, n // i])  # Positive divisors

    divisors.update([-x for x in divisors])  # Negative divisors

    return divisors


# gcd of Terms
def get_common_terms(a: Term, b: Term):
    common_coeff = common_base = common_exp = 1

    if type(a.coefficient) == int and type(b.coefficient) == int:
        common_coeff = gcd(a.coefficient, b.coefficient)
    else:
        pass  # TODO: accommodate other types

    if a.base == b.base:
        common_base = a.base

        if type(a.coefficient) == int and type(b.coefficient) == int:
            common_exp = min(a.exponent, b.exponent)

    return Term(common_coeff, common_base, common_exp)


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

# for e in equations:
#     print(e, "Roots:", get_real_roots(e), sep="\t")
#     print()
