from number_functions import greatest_common_divisor as gcd


# ax^p      All terms must be integers
class Term:
    def __init__(self, coeff, exp, var_name="x"):
        self.coefficient = coeff
        self.exponent = exp
        self.var_name = var_name
        self.is_positive = coeff >= 0

    def __mul__(self, other):
        return Term(self.coefficient * other.coefficient, self.exponent + other.exponent)

    def __truediv__(self, other):
        return Term(self.coefficient / other.coefficient, self.exponent - other.exponent)

    def __add__(self, other):
        if self.exponent != other.exponent:
            raise ArithmeticError("Can't add terms of differing exponents: {}, {}".format(self, other))

        if self.var_name != other.var_name:
            raise ArithmeticError("Can't add terms of differing bases: {}, {}".format(self, other))

        return Term(self.coefficient + other.coefficient, self.exponent)

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        return Term(-self.coefficient, self.exponent, self.var_name)

    def __repr__(self):
        return "{}{}*{}**{}".format("+" if self.coefficient > 0 else "",
                                    self.coefficient if type(self.coefficient) == int else "({})".format(
                                        self.coefficient),
                                    self.var_name,
                                    self.exponent if type(self.exponent) == int else "({})".format(self.exponent))


# a/b       All terms must be integers
class Fraction:
    def __init__(self, numerator, denominator):
        # Combines fractions if not a/b where a,b are integers
        if type(numerator) == Fraction or type(denominator) == Fraction:
            numerator = Fraction(numerator, 1) if type(numerator) == int else numerator
            denominator = Fraction(denominator, 1) if type(denominator) == int else denominator
            new_fraction = numerator / denominator
            numerator = new_fraction.numerator
            denominator = new_fraction.denominator

        self.numerator = numerator
        self.denominator = denominator
        self.simplify()

    def __mul__(self, other):
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        return Fraction(self.numerator * other.denominator, other.numerator * self.denominator)

    def __add__(self, other):
        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __sub__(self, other):
        return self.__add__(other.__neg__())

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def __repr__(self):
        return "{} / {}".format(self.numerator, self.denominator)

    def __lt__(self, other):
        return self.__float__() < other

    def __gt__(self, other):
        return self.__float__() > other

    def __le__(self, other):
        return self.__float__() <= other

    def __ge__(self, other):
        return self.__float__() >= other

    def __eq__(self, other):
        return self.__float__() == other

    def __float__(self):
        return self.numerator / self.denominator

    def simplify(self):
        div = gcd(self.numerator, self.denominator)
        self.numerator //= div
        self.denominator //= div


# Sequence of terms
class Expression:
    def __init__(self, *terms):
        self.terms = sorted([*terms], key=lambda t: t.exponent, reverse=True)

    def __repr__(self):
        return " ".join(list(map(str, self.terms)))
