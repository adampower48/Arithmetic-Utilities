from math import sqrt

import matrix_functions as mf


class Matrix:
    def __init__(self, rows):
        self.rows = list(rows)

        self.num_rows = len(self.rows)
        self.num_cols = len(self.rows[0])

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
        max_num_size = 0
        for row in self.rows:
            for entry in row:
                l = len(str(entry))
                if l > max_num_size:
                    max_num_size = l

        num_format = lambda n: "{:>{}}".format(n, max_num_size)

        return "\n".join("  ".join(list(map(num_format, r))) for r in self.rows)

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

    def transpose(self):
        return Matrix(list(zip(*self.rows)))

    def sub_matrix(self, row_rem, col_rem):
        # Returns matrix with given row & column removed
        return Matrix([[self.rows[i][j] for j in range(self.num_cols) if j != col_rem]
                       for i in range(self.num_rows) if i != row_rem])

    def swap_rows(self, i1, i2):
        self.rows[i1], self.rows[i2] = self.rows[i2], self.rows[i1]

    def scale_row(self, i, s):
        self.rows[i] = [self.rows[i][j] * s for j in range(self.num_cols)]
        mf.round_matrix(self)

    def add_row(self, i, k, s=1):
        self.rows[i] = [self.rows[i][j] + s * self.rows[k][j] for j in range(self.num_cols)]

    def is_zero(self):
        for row in self.rows:
            for entry in row:
                if entry:
                    return False

        return True

    def is_identity(self):
        if self.num_rows != self.num_cols:
            return False

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if i == j and self.rows[i][j] != 1:
                    return False
                elif i != j and self.rows[i][j] != 0:
                    return False

        return True


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

    def dot_product(self, other):
        if self.num_rows == other.num_rows == 1:  # row vectors
            return sum([self.rows[0][i] * other.rows[0][i] for i in range(self.num_cols)])

        elif self.num_cols == other.num_cols == 1:  # column vectors
            return sum([self.rows[i][0] * other.rows[i][0] for i in range(self.num_rows)])

        elif self.num_cols == other.num_rows == 1 or self.num_rows == other.num_cols == 1:  # col/row vector combination
            return self.transpose().dot_product(other)

        else:
            raise ArithmeticError("Dot Product unavailable for matrix dimensions: {}x{} and {}x{}".format(
                self.num_rows, self.num_cols, other.num_rows, other.num_cols))


def get_unit_vectors(dimensions):
    vectors = [[0] * dimensions] * dimensions
    for i, v in enumerate(vectors):
        v[i] = 1

    return vectors


def get_identity_matrix(n):
    rows = [[0] * n] * n
    for i in range(n):
        rows[i][i] = 1

    return Matrix(rows)


def read_matrix():
    m, n = map(int, input("Dimensions M N >").split())
    rows = [list(map(int, input("Row {}:".format(i + 1)).split())) for i in range(m)]
    print(*rows)
    return Matrix(rows)
