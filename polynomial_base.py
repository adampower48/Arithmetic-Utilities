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
        if other == 0:
            return self

        if self.exponent != other.exponent:
            raise ArithmeticError("Can't add terms of differing exponents: {}, {}".format(self, other))

        if self.var_name != other.var_name:
            raise ArithmeticError("Can't add terms of differing bases: {}, {}".format(self, other))

        return Term(self.coefficient + other.coefficient, self.exponent)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        return Term(-self.coefficient, self.exponent, self.var_name)

    def __eq__(self, other):
        if type(other) == Term:
            return self.coefficient == other.coefficient and self.exponent == other.exponent

        if self.exponent == 0:
            return self.coefficient == other

        if self.coefficient == 0:
            return other == 0

        return False

    def __repr__(self):
        sign = "+" if self.coefficient >= 0 else ""

        if type(self.coefficient) == int:
            coeff = "" if self.coefficient == 1 and self.exponent != 0 else self.coefficient
        else:
            coeff = "({})".format(self.coefficient)

        var = "" if self.exponent == 0 else self.var_name

        if type(self.exponent) == int:
            exp = "" if self.exponent == 0 else self.exponent
        else:
            exp = "({})".format(self.exponent)

        return "{}{}{}{}{}".format(sign, coeff, var, "^" if self.exponent != 0 else "", exp)


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

    def __hash__(self):
        return hash((self.numerator, self.denominator))

    def __mul__(self, other):
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        return Fraction(self.numerator * other.denominator, other.numerator * self.denominator)

    def __add__(self, other):
        if type(other) == int:
            other = Fraction(other, 1)

        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __sub__(self, other):
        return self.__add__(-other)

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

    def __ne__(self, other):
        return self.__float__() != other

    def __float__(self):
        return self.numerator / self.denominator

    def simplify(self):
        div = gcd(self.numerator, self.denominator)
        self.numerator //= div
        self.denominator //= div


# Sequence of terms
class Expression:
    def __init__(self, *terms):
        self.terms = [*terms]
        self.simplify()
        self.terms.sort(key=lambda t: t.exponent, reverse=True)

    def __add__(self, other):
        if type(other) == Expression:
            return Expression(*self.terms, *other.terms)

        if type(other) == Term:
            return Expression(*self.terms, other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        terms = []
        for t1 in self.terms:
            for t2 in other.terms:
                terms.append(t1 * t2)

        return Expression(*terms)

    def __neg__(self):
        return Expression(*[-t for t in self.terms])

    def __repr__(self):
        return " ".join(list(map(str, self.terms)))

    def simplify(self):
        terms = []

        for e in set(t.exponent for t in self.terms):
            tmp_terms = [t for t in self.terms if t.exponent == e]
            if len(tmp_terms) > 0:
                if sum(tmp_terms) != 0:
                    terms.append(sum(tmp_terms))

        self.terms = terms
