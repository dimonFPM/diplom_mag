import math


def f1(p, s, w, e, jj, x, c):
    return ((p * s * w ** 2) / (e * jj) - ((c * x ** 4) / (e * jj))) ** (1 / 4)


for x in range(10):
    print(f1(1, 1, 1, 1, 1, x, 0))
