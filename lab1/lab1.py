def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    d, x1, y1 = extended_gcd(b % a, a)
    return (d, y1 - (b // a) * x1, x1)


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def binary_gcd(a, b):
    if a == b or b == 0:
        return a
    if a == 0:
        return b
    if a % 2 == 0:
        if b % 2 == 0:
            return binary_gcd(a // 2, b // 2) * 2
        else:
            return binary_gcd(a // 2, b)
    if b % 2 == 0:
        return binary_gcd(a, b // 2)
    if a > b:
        return binary_gcd((a - b) // 2, b)
    return binary_gcd((b - a) // 2, a)


def find_comparison_solution(a, b, m):
    d = gcd(a, m)
    a = a // d
    b = b // d
    m = m // d
    x = extended_gcd(a, m)[1] * b % m
    if x < 0:
        x = m + x
    return x


def check_coprime(m):
    for i in range(len(m)):
        for j in range(len(m)):
            if i != j and gcd(m[i], m[j]) != 1:
                return False
    return True


def first_theorem(u, m, M):
    x = 0
    for i in range(len(m)):
        c = M // m[i]
        d = find_comparison_solution(c, 1, m[i])
        x += c * d * u[i]
    return x % M


def garner_algorithm(u, m):
    c = [[0 for _ in m] for _ in m]
    for i in range(len(m)):
        for j in range(len(m)):
            c[i][j] = find_comparison_solution(m[i], 1, m[j])
    q = [0 for _ in m]

    for i in range(len(m)):
        q[i] = u[i]
        for j in range(i):
            q[i] = c[j][i] * (q[i] - q[j])
            q[i] = q[i] % m[i]
            if q[i] < 0:
                q[i] += m[i]
    m_iter = 1
    x = 0
    for i in range(len(m)):
        x += q[i] * m_iter
        m_iter *= m[i]
    return x, q


def swap_rows(A, B, row1, row2):
    A[row1], A[row2] = A[row2], A[row1]
    B[row1], B[row2] = B[row2], B[row1]


def divide_row(A, B, row, divider, m):
    A[row] = [find_comparison_solution(divider, a, m) for a in A[row]]
    B[row] = find_comparison_solution(divider, B[row], m)


def combine_rows(A, B, row, source_row, weight, m):
    A[row] = [(a + (k * weight) % m) % m for a, k in zip(A[row], A[source_row])]
    B[row] = (B[row] + (B[source_row] * weight) % m) % m


def drop_trivial_row(A, B):
    A1, B1 = [], []
    for i in range(len(A)):
        f = False
        for j in range(len(A[i])):
            if A[i][j] != 0:
                f = True
        if f:
            A1.append(A[i])
            B1.append(B[i])
    return A1, B1


def gauss_algorithm(A, B, m):
    column = 0
    while column < len(B):
        current_row = None
        for r in range(column, len(A)):
            if current_row is None or abs(A[r][column]) > abs(A[current_row][column]):
                current_row = r
        if current_row is None:
            print("No solutions!")
            return None
        if current_row != column:
            swap_rows(A, B, current_row, column)
        if A[column][column] != 0:
            divide_row(A, B, column, A[column][column], m)
        for r in range(column + 1, len(A)):
            combine_rows(A, B, r, column, -A[r][column], m)
        for r in range(0, column):
            combine_rows(A, B, r, column, -A[r][column], m)
        A, B = drop_trivial_row(A, B)
        column += 1
    return A, B


def check_solution_exist(B):
    solution = False
    for i in range(len(B) - 1):
        if B[i] != 0:
            solution = True
    return solution


def task1():
    a, b = map(int, input("Enter a and b : ").split(" "))
    print(f"GCD = {gcd(a, b)}")
    print(
        "Extended GCD:\n{res[1]} * {a} + {res[2]} * {b} = {res[0]}".format(
            res=extended_gcd(a, b), a=a, b=b
        )
    )
    print(f"Binary GCD = {binary_gcd(a, b)}")


def task2():
    n = int(input("Enter number of comparisons: "))
    u, m, M = [], [], 1
    comp = ""
    print("Enter comparisons (format u m)")
    for _ in range(n):
        u_i, m_i = map(int, input().split(" "))
        comp += f"x ≡ {u_i} (mod {m_i})\n"
        M *= m_i
        u.append(u_i)
        m.append(m_i)
    print("Your system of comparisons")
    print(comp)
    if check_coprime(m):
        print(f"x = {first_theorem(u, m, M)}")
        print("Garner's algorithm:")
        x, q = garner_algorithm(u, m)
        print(f"q : {q}\nx = {x}")
    else:
        print("The bases of the system are not relatively prime!")


def task3():
    rows = int(input("Enter number of rows:"))
    print("Enter matrix of odds")
    A = [list(map(int, (input(f"row {i+1}: ").split()))) for i in range(rows)]
    B = list(map(int, input("Enter free terms of the equation: ").split()))
    m = int(input("Enter field dimension: "))
    ans = gauss_algorithm(A, B, m)
    if ans:
        A, B = ans
        if check_solution_exist(B):
            for i in range(len(A)):
                ans_str = f"x_{i+1}="
                for j in range(len(A[i]) - len(A), len(A[i])):
                    ans_str += f"{-A[i][j] % m}*x_{j+1}+"
                ans_str += f"{B[i]}"
                print(ans_str)
        else:
            print("No solutions!")


task3()
