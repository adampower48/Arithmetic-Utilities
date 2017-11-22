from math import sqrt


class Matrix:
    def __init__(self, rows):
        self.rows = list(rows)
        self.cols = list(zip(*self.rows))

        self.num_rows = len(self.rows)
        self.num_cols = len(self.cols)

    def __mul__(self, other):
        if type(other) == Matrix:
            return self.matrix_mul(other)
        if type(other) in [int, float]:
            return self.scalar_mul(other)

        raise TypeError("Multiplication unsupported for types: {} and {}".format(type(self), type(other)))

    def __add__(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ArithmeticError(
                "Can't add matrices of differing dimensions: {}x{} and {}x{}".format(self.num_rows, self.num_cols,
                                                                                     other.num_rows, other.num_cols))

        new_rows = [[self.rows[i][j] + other.rows[i][j] for j in range(self.num_cols)] for i in range(self.num_rows)]
        return Matrix(new_rows)

    def __repr__(self):
        return "\n".join("\t\t".join(list(map(str, r))) for r in self.rows)

    def scalar_mul(self, c):
        new_rows = [[self.rows[i][j] * c for j in range(self.num_cols)] for i in range(self.num_rows)]
        return Matrix(new_rows)

    def matrix_mul(self, other):
        if self.num_cols != other.num_rows:
            raise ArithmeticError(
                "Can't multiple Matrices: {}x{} and {}x{}".format(self.num_rows, self.num_cols, other.num_rows,
                                                                  other.num_cols))

        new_rows = []
        for a in range(self.num_rows):
            new_rows.append([])
            for b in range(other.num_cols):
                entry = sum([self.rows[a][i] * other.rows[i][b] for i in range(self.num_cols)])
                new_rows[a].append(entry)

        return Matrix(new_rows)

    def dot_product(self, other):
        if self.num_rows == other.num_rows == 1:  # row vectors
            return sum([self.rows[0][i] * other.rows[0][i] for i in range(self.num_cols)])

        elif self.num_cols == other.num_cols == 1:  # column vectors
            return sum([self.rows[i][0] * other.rows[i][0] for i in range(self.num_rows)])

        elif self.num_cols == other.num_rows == 1 or self.num_rows == other.num_cols == 1:  # col/row vector combination
            return self.transpose().dot_product(other)

        else:
            raise ArithmeticError(
                "Dot Product unavailable for matrix dimensions: {}x{} and {}x{}".format(self.num_rows, self.num_cols,
                                                                                        other.num_rows, other.num_cols))

    def transpose(self):
        return Matrix(self.cols)

    def inverse(self):
        if self.num_rows != 2 and self.num_cols != 2:
            raise TypeError("Inverse unsupported for matrix dimensions: {}x{}".format(self.num_rows, self.num_cols))

        if self.determinant() == 0:
            raise ArithmeticError("Matrix has no inverse: determinant = 0")

        return self.adjugate() * (1 / self.determinant())

    def determinant(self):
        if self.num_rows != 2 and self.num_cols != 2:
            raise TypeError("Determinant unsupported for matrix dimensions: {}x{}".format(self.num_rows, self.num_cols))

        return self.rows[0][0] * self.rows[1][1] - self.rows[0][1] * self.rows[1][0]

    def adjugate(self):
        if self.num_rows != 2 and self.num_cols != 2:
            raise TypeError("Adjugate unsupported for matrix dimensions: {}x{}".format(self.num_rows, self.num_cols))

        new_rows = [[self.rows[1][1], -self.rows[0][1]], [-self.rows[1][0], self.rows[0][0]]]
        return Matrix(new_rows)


class Vector(Matrix):
    def __init__(self, values):
        super().__init__([[v] for v in values])

    def magnitude(self):
        return sqrt(sum(x[0] ** 2 for x in self.rows))

    # Applicable for 3 dimensions only.
    def cross_product(self, other):
        assert len(self.rows) == len(other.rows) and len(self.rows[0]) == len(other.rows[0])

        unit_vectors = get_unit_vectors(len(self.rows))
        # todo: finish cross product


def get_unit_vectors(dimensions):
    vectors = [[0] * dimensions] * dimensions
    for i, v in enumerate(vectors):
        v[i] = 1

    return vectors


def read_matrix():
    m, n = map(int, input("Dimensions M N >").split())
    rows = [list(map(int, input("Row {}:".format(i + 1)).split())) for i in range(m)]
    print(*rows)
    return Matrix(rows)
