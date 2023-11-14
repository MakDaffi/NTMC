import random


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def jacobi(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        n = n % 8
        if n == 3 or n == 5:
            return -1
        else:
            return 1
    if a % 2 == 0:
        return jacobi(2, n) * jacobi(a // 2, n)
    if a >= n:
        return jacobi(a % n, n)
    if a % 4 == 3 and n % 4 == 3:
        return -jacobi(n, a)
    else:
        return jacobi(n, a)


def miller_rabin_test(p: int, k: int = 100) -> bool:
    if not p % 2:
        return False
    t = p - 1
    s = 0
    while t % 2 == 0:
        t //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, p - 1)
        x = pow(a, t, p)
        if x != 1 and x != p - 1:
            for _ in range(s - 1):
                x = x**2 % p
                if x == 1 or x == p - 1:
                    return False
    return True


def solovey_strassen_test(p: int, k: int = 100) -> bool:
    for _ in range(k):
        a = random.randint(2, p - 1)
        if gcd(a, p) != 1:
            return False
        if pow(a, (p - 1) // 2, p) != jacobi(a, p) % p:
            return False
    return True


def ferma_test(p: int, k: int = 100) -> bool:
    for _ in range(k):
        a = random.randint(2, p - 1)
        if gcd(p, a) > 1:
            return False
    if pow(a, p - 1, p) != 1:
        return False
    return True


def main():
    p = int(input("Введите число p: "))
    k = int(input("Введите количество раундов k: "))
    print(f"Тест Ферма: {ferma_test(p, k)}")
    print(f"Тест Соловея — Штрассена: {solovey_strassen_test(p,k)}")
    print(f"Тест Миллера-Рабина: {miller_rabin_test(p, k)}")


if __name__ == "__main__":
    main()
