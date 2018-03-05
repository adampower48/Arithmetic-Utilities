import functools
from copy import deepcopy
from random import randrange

import matrix_base as mb
from number_functions import lowest_common_multiple, greatest_common_divisor


def row_echelon(A: mb.Matrix):
    # A: Augmented matrix representing linear system
    # todo: fix bug giving incorrect resulting matrix

    A = deepcopy(A)

    for k in range(min(A.num_rows, A.num_cols)):
        # Find k-th pivot
        i_max = max([i for i in range(k, A.num_rows)], key=lambda e: abs(A.rows[e][k]))
        if A.rows[i_max][k] == 0:
            print("Matrix is singular!")

        A.rows[i_max], A.rows[k] = A.rows[k], A.rows[i_max]

        # Do for all rows below pivot
        for i in range(k + 1, A.num_rows):
            f = A.rows[i][k] / A.rows[k][k]
            # Do for all remaining elements in current row
            for j in range(k + 1, A.num_cols):
                A.rows[i][j] -= A.rows[k][j] * f

            # Fill lower triangular matrix with 0's
            A.rows[i][k] = 0

    return A


def row_echelon_int(M: mb.Matrix):
    # Transforms matrix to REF keeping the entries as integers

    M = deepcopy(M)
    # print("Start:", M, sep="\n")

    min_i = 0
    min_j = 0
    while min_i < M.num_rows and min_j < M.num_cols:
        # print("Iteration", min_i, ":")
        # Send 0 starting rows to bottom
        sort_matrix(M)
        num_zeros = count_zero_rows(M)

        # print("After moving 0 rows:", M, sep="\n")

        # Increase rows to lcm
        nz_col = [M.rows[i][min_j] for i in range(min_i, M.num_rows - num_zeros) if M.rows[i][min_j] != 0]
        lcm = lowest_common_multiple(*nz_col)
        for i in range(min_i, min_i + len(nz_col)):
            factor = lcm // M.rows[i][min_j]
            M.scale_row(i, factor)

        # print("After scaling up col by {}:".format(lcm), M, sep="\n")

        # Subtract 1st row from all below rows
        for i in range(min_i + 1, min_i + len(nz_col)):
            M.add_row(i, min_i, -1)

        # print("After subtracting under pivot:", M, sep="\n")

        # Reduce first row
        nz_row = [e for e in M.rows[min_i] if e != 0]
        gcd = greatest_common_divisor(*nz_row)
        M.scale_row(min_i, 1 / gcd)
        if M.rows[min_i][min_j] < 0:  # Make positive
            M.scale_row(min_i, -1)

        # print("After cleaning first row:", M, sep="\n")

        min_i += 1
        min_j += 1

    return M


def reduced_row_echelon_int(M: mb.Matrix):
    # Given result from row_echelon_int
    # Transforms REF matrix into Reduced REF

    M = deepcopy(M)
    # print("Start:", M, sep="\n")

    num_zeros = count_zero_rows(M)

    for i in range(M.num_rows - num_zeros - 1, -1, -1):
        pivot_col_j = next(j for j in range(M.num_cols) if M.rows[i][j] != 0)

        # Scaling pivots to lcm
        nz_pivot_col = [M.rows[_i][pivot_col_j] for _i in range(M.num_rows) if M.rows[_i][pivot_col_j] != 0]
        lcm = lowest_common_multiple(*nz_pivot_col)
        for _i in range(i + 1):
            factor = lcm // M.rows[_i][pivot_col_j]
            M.scale_row(_i, factor)

        # print("After pivot col {} scaled to lcm:".format(pivot_col_j), M, sep="\n")

        # Subtracting pivot row from above rows
        for _i in range(i):
            M.add_row(_i, i, -1)

        # print("After pivot row subtracted from above:", M, sep="\n")

        # Reduce pivot row
        nz_row = [e for e in M.rows[i] if e != 0]
        gcd = greatest_common_divisor(*nz_row)
        M.scale_row(i, 1 / gcd)
        if M.rows[i][pivot_col_j] < 0:  # Make positive
            M.scale_row(i, -1)

            # print("After pivot row cleaned up:", M, sep="\n")

    return M


def reduced_row_echelon(A: mb.Matrix):
    # A: Augmented matrix representing linear system
    A = row_echelon(A)

    for i in range(A.num_cols - 2, -1, -1):
        A.rows[i][-1] /= A.rows[i][i]
        A.rows[i][i] = 1
        f = A.rows[i][-1]

        for k in range(i):
            A.rows[k][-1] -= A.rows[k][i] * f
            A.rows[k][i] = 0

    return A


def hermite_normal_form(M: mb.Matrix):
    # https://en.wikipedia.org/wiki/Hermite_normal_form

    if M.is_zero():
        return M

    print("Start:", M, sep="\n")

    M = deepcopy(M)

    # Send 0 starting rows to bottom
    i = 0
    num_zeros = 0
    while i < M.num_rows - num_zeros:
        if M.rows[i][0] == 0:
            print("Swapping rows:", i, M.rows[i], ",", M.num_rows - num_zeros - 1, M.rows[M.num_rows - num_zeros - 1])
            M.swap_rows(i, M.num_rows - num_zeros - 1)
            num_zeros += 1
        i += 1

    # Increase rows to lcm
    nz_col = [M.rows[i][0] for i in range(M.num_rows - num_zeros)]
    lcm = lowest_common_multiple(*nz_col)
    for i in range(M.num_rows - num_zeros):
        factor = lcm // nz_col[i]
        print("Multiplying row by", factor, ":", i, M.rows[i], "->", end=" ")
        M.scale_row(i, factor)
        print(M.rows[i])

    # Subtract 1st row from all below rows
    print("Subtracting row:", 0, M.rows[0])
    for i in range(1, M.num_rows - num_zeros):
        print("\t", M.rows[i], "->", end=" ")
        M.add_row(i, 0, -1)
        print(M.rows[i])

    # Clean up 1st row
    gcd = greatest_common_divisor(*M.rows[0])
    print("Scaling row by 1 /", gcd, ":", M.rows[0], "->", end=" ")
    M.scale_row(0, 1 / gcd)
    if M.rows[0][0] < 0:
        M.scale_row(0, -1)
    print(M.rows[0])

    # Calculation and insertion of the sub-matrix in H-normal form
    print("---")
    sub = hermite_normal_form(M.sub_matrix(0, 0))
    for i in range(sub.num_rows):
        for j in range(sub.num_cols):
            M.rows[1 + i][1 + j] = sub.rows[i][j]

    return M


def round_matrix(M: mb.Matrix, decimal_threshold=6):
    for i in range(M.num_rows):
        for k in range(M.num_cols):
            if abs(round(M.rows[i][k]) - M.rows[i][k]) < 0.1 ** -decimal_threshold:
                M.rows[i][k] = round(M.rows[i][k])


def determinant(M: mb.Matrix):
    # Determinant of given matrix by expansion along first column
    if M.num_rows == 1:
        return M.rows[0][0]

    return sum(
        ((-1) ** i) * M.rows[i][0] * determinant(M.sub_matrix(i, 0))
        for i in range(M.num_rows)
    )


def adjugate(M: mb.Matrix):
    return cofactors(M).transpose()


def cofactors(M: mb.Matrix):
    return mb.Matrix(
        [[((-1) ** (i + j)) * determinant(M.sub_matrix(i, j))
          for j in range(M.num_cols)]
         for i in range(M.num_rows)]
    )


def inverse(M: mb.Matrix):
    if M.num_rows != M.num_cols:
        # raise ArithmeticError("Invalid size for invertible matrix: {}x{}. Must be square.".format(
        # M.num_rows, M.num_cols))
        return None

    det = determinant(M)
    if det == 0:
        # raise ArithmeticError("Matrix has no inverse: determinant = 0")
        return None

    return adjugate(M) * (1 / det)


def sort_matrix(M: mb.Matrix):
    # Roughly sorts rows of a matrix, putting 0 rows at the bottom
    M.rows.sort(key=functools.cmp_to_key(cmp_rows))


def cmp_rows(r1, r2):
    # Used to sort zero rows to bottom

    for a, b in zip(r1, r2):
        # 0's are considered larger than other numbers
        if a == 0 and b != 0:
            return 1
        if b == 0 and a != 0:
            return -1

        if a > b:
            return 1
        if a < b:
            return -1

    return 0


def count_zero_rows(M: mb.Matrix):
    zeros = 0
    for row in M.rows:
        if row.count(0) == M.num_cols:
            zeros += 1

    return zeros


def gen_random_matrix(row_range=range(2, 11), col_range=range(2, 11), num_range=range(-100, 101)):
    num_rows = range(randrange(row_range.start, row_range.stop, row_range.step))
    num_cols = range(randrange(col_range.start, col_range.stop, col_range.step))
    return mb.Matrix([[randrange(num_range.start, num_range.stop, num_range.step)
                       for j in num_cols] for i in num_rows])
