import math

e = 1
j = 1
m = 1
l = 1
k = 1
for k in range(1, 11):
    # print(f"k={k}")
    # print(((math.pi ** 2 * k ** 2) / l ** 2) * math.sqrt(e * j / m))
    print(((math.pi ** 2 * (1 / 4 + k + k ** 2)) / l ** 2) * math.sqrt(e * j / m))
