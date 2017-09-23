# ax^p      All terms must be integers
class Term:
    def __init__(self, coeff=1, exp=1, var_name="x"):
        self.coefficient = coeff
        self.exponent = exp
        self.var_name = var_name
        self.is_positive = coeff >= 0

    def __mul__(self, other):
        return Term(self.coefficient * other.coefficient, self.exponent + other.exponent)

    def __add__(self, other):
        if self.exponent != other.exponent:
            raise ArithmeticError("Can't add terms of differing exponents: {}, {}".format(self, other))

        if self.var_name != other.var_name:
            raise ArithmeticError("Can't add terms of differing bases: {}, {}".format(self, other))

        return Term(self.coefficient + other.coefficient, self.exponent)

    def __repr__(self):
        return "{}{}*{}**{}".format("+" if self.is_positive else "", self.coefficient, self.var_name, self.exponent)


# a/b       All terms must be integers
class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __mul__(self, other):
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __add__(self, other):
        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __sub__(self, other):
        return self.__add__(other.__neg__())

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def decimal_value(self):
        return self.numerator / self.denominator
