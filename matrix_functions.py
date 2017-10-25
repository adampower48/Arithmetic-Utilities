from copy import deepcopy

from matrix_base import Matrix


def row_echelon(A: Matrix):
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


def reduced_row_echelon(A):
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


def round_matrix(M: Matrix, decimal_threshold=6):
    for i in range(M.num_rows):
        for k in range(M.num_cols):
            if abs(round(M.rows[i][k]) - M.rows[i][k]) < 0.1 ** -decimal_threshold:
                M.rows[i][k] = round(M.rows[i][k])
