from sys import stderr

from number_functions import greatest_common_divisor as gcd


# ax^p      All terms must be integers
class Term:
    def __init__(self, coeff, exp, var_name="x"):
        self.coefficient = coeff
        self.exponent = exp
        self.var_name = var_name
        self.is_positive = coeff >= 0

    def __mul__(self, other):
        if type(other) == int:
            return Term(self.coefficient * other, self.exponent)
        return Term(self.coefficient * other.coefficient, self.exponent + other.exponent)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if type(other) in [int, Fraction]:
            return Term(Fraction(self.coefficient, other), self.exponent)
        return Term(Fraction(self.coefficient, other.coefficient), self.exponent - other.exponent)

    def __rtruediv__(self, other):
        if type(other) in [int, Fraction]:
            return Term(other, 0, self.var_name) / self

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
        if type(other) == float or type(other) == int:
            return Fraction(self.numerator * other, self.denominator)

        if type(other) == Irrational:
            return Irrational(self * other.coefficient, other.base, other.exponent)

        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if type(other) == Fraction:
            return Fraction(self.numerator * other.denominator, other.numerator * self.denominator)
        if type(other) == Term:
            return other.__rtruediv__(self)

    def __pow__(self, power, modulo=None):
        return Fraction(self.numerator ** power, self.denominator ** power)

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
        if self.denominator == 1:
            return str(self.numerator)
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
        # 2/6   ->  1/3
        div = gcd(self.numerator, self.denominator)
        self.numerator //= div
        self.denominator //= div

        # Ensures - sign is on top of fraction if negative  12/-5   ->  -12/5
        if self.numerator / self.denominator < 0 and self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

            # if self.denominator == 1:
            #     print(self, "can be converted to", self.numerator)


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

    # TODO: division

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


# a^b
class Irrational:
    def __init__(self, coeff, base, exponent):
        self.base = base
        self.exponent = exponent
        self.coefficient = coeff

    def __add__(self, other):
        if type(other) == Irrational and other.base == self.base and other.exponent == self.exponent:
            return Irrational(self.coefficient + other.coefficient, self.base, self.exponent)

        print("Unsupported operation add for: {}, {}".format(self, other), file=stderr)

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        return Irrational(-self.coefficient, self.base, self.exponent)

    def __mul__(self, other):
        if type(other) == Irrational:
            if other.exponent == self.exponent:
                return Irrational(self.coefficient * other.coefficient, self.base * other.base, self.exponent)
            if other.base == self.base:
                return Irrational(self.coefficient * other.coefficient, self.base, self.exponent + other.exponent)

        if type(other) == int or type(other) == Fraction:
            return Irrational(self.coefficient * other, self.base, self.exponent)

    def __truediv__(self, other):
        if type(other) == Irrational:
            if other.exponent == self.exponent:
                return Irrational(Fraction(self.coefficient, other.coefficient), Fraction(self.base, other.base),
                                  self.exponent)

            if other.base == self.base:
                return Irrational(Fraction(self.coefficient, other.coefficient), self.base,
                                  self.exponent - other.exponent)

        if type(other) == int or type(other) == Fraction:
            return Irrational(Fraction(self.coefficient, other), self.base, self.exponent)

    def __pow__(self, power, modulo=None):
        if type(power) == Fraction or type(power) == Irrational:
            new_coeff = Irrational(1, self.coefficient, power)
        elif power < 0:
            new_coeff = Fraction(1, self.coefficient ** -power)
        else:
            new_coeff = self.coefficient ** power

        return Irrational(new_coeff, self.base, self.exponent * power)

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
        return self.coefficient * self.base ** float(self.exponent)

    def __repr__(self):
        sign = "+" if self.coefficient >= 0 else ""

        if type(self.coefficient) == int:
            coeff = "" if self.coefficient == 1 and self.exponent != 0 else "{}*".format(self.coefficient)
        else:
            coeff = "" if self.coefficient == 1 and self.exponent != 0 else "({})*".format(self.coefficient)

        var = self.base if type(self.base) == int else "({})".format(self.base)

        if type(self.exponent) == int:
            exp = "" if self.exponent == 0 else self.exponent
        else:
            exp = "({})".format(self.exponent)

        if self.coefficient == 0:
            return "+0"

        if self.base == 1 or self.exponent == 0:
            return "{}{}".format(sign, self.coefficient)

        return "{}{}{}{}{}".format(sign, coeff, var, "^" if self.exponent != 0 else "", exp)
