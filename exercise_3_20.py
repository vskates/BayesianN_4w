def outer(a, b):
    m = []
    for i in range(len(a)):
        row = []
        for j in range(len(b)):
            row.append(a[i] * b[j])
        m.append(row)
    return m


def add_matrices(A, B):
    n = len(A)
    m = len(A[0])
    C = []

    for i in range(n):
        row = []
        for j in range(m):
            row.append(A[i][j] + B[i][j])
        C.append(row)

    return C


def scale_matrix(A, c):
    B = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[i])):
            row.append(c * A[i][j])
        B.append(row)
    return B


def row_sums(A):
    s = []
    for row in A:
        s.append(sum(row))
    return s


def col_sums(A):
    if not A:
        return []

    s = [0.0] * len(A[0])
    for i in range(len(A)):
        for j in range(len(A[i])):
            s[j] += A[i][j]
    return s


def exercise_3_20_joint():
    p_inc_low = 0.8
    p_inc_high = 0.2

    p_w_low = [0.7, 0.3, 0.0, 0.0]
    p_w_high = [0.2, 0.1, 0.4, 0.3]

    p_h_low = [0.2, 0.8, 0.0, 0.0]
    p_h_high = [0.0, 0.0, 0.3, 0.7]

    low_part = scale_matrix(outer(p_w_low, p_h_low), p_inc_low)
    high_part = scale_matrix(outer(p_w_high, p_h_high), p_inc_high)

    return add_matrices(low_part, high_part)


def exercise_3_20_marginals():
    joint = exercise_3_20_joint()
    p_w = row_sums(joint)
    p_h = col_sums(joint)
    return p_w, p_h


def independent(joint, eps=1e-12):
    p_w = row_sums(joint)
    p_h = col_sums(joint)

    for i in range(len(joint)):
        for j in range(len(joint[i])):
            if abs(joint[i][j] - p_w[i] * p_h[j]) > eps:
                return False

    return True


def solve_exercise_3_20():
    joint = exercise_3_20_joint()
    p_w, p_h = exercise_3_20_marginals()

    return {
        "p(w,h)": joint,
        "p(w)": p_w,
        "p(h)": p_h,
        "independent": independent(joint),
    }


def _round_row(row, digits=3):
    return [round(x, digits) for x in row]


if __name__ == "__main__":
    ans = solve_exercise_3_20()

    print("p(w,h) =")
    for row in ans["p(w,h)"]:
        print(_round_row(row))

    print("\np(w) =", _round_row(ans["p(w)"]))
    print("p(h) =", _round_row(ans["p(h)"]))
    print("h independent of w? ", ans["independent"])
