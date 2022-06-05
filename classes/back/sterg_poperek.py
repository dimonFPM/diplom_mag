import datetime
import tkinter
import datetime as dt
import math
import time
import cmath as cm
# import numba
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from tqdm import *


# region поперчно-изгибные колебания стержня
def get_values(*names):
    try:
        value_list = [float(i.get()) for i in names if i.get() != ""]
    except:
        print("не число")
        return None
    if len(names) == len(value_list):
        return value_list
    else:
        print("одно из полей не заполнено")
        return None


def frequency0(k):
    if k == 1:
        return 1.875
    elif k == 2:
        return 4.694
    elif k == 3:
        return 7.855
    elif k == 4:
        return 10.996
    elif k == 5:
        return 14.137
    elif k == 6:
        return 17.279


def frequency1(k):
    return math.pi / 2 + math.pi * k


def frequency2(k):  # sin
    return math.pi * k


def frequency3(k):
    # if k == 1:
    #     return 1.46946
    # elif k == 2:
    #     return 4.61446
    # elif k == 3:
    #     return 4.99379
    if k == 1:
        return 0.32477
    elif k == 2:
        return 1.45742
    elif k == 3:
        return 4.71046


# def frequency3(p, s, e, j, c0, cz, len_sterg):
#     lx = []
#     ly = []
#     n = (cz * len_sterg ** 3) / e * j
#     for x in np.arange(0, 100, 0.001):
#         # la = compute_a2(p, s, x, e, j, c0, len_sterg)  # x частота
#         kk = x ** 3 / n
#         slog1 = 2 * kk * math.sin(x) * math.sinh(x)
#         slog2 = 2 * kk * (math.sinh(x) * math.cos(x) - math.sin(x) * math.cosh(x))
#         slog3 = kk ** 2 * (1 - math.cosh(x) * math.cos(x))
#         lx.append(x)
#         ly.append(slog1 + slog2 + slog3)
#     return lx, ly


def compute_frequency0(l, e, j, m, k):  # защем
    fre = frequency0(k)
    print(fre)
    return (((fre ** 2) / l ** 2) * math.sqrt(e * j / m))


def compute_frequency1(l, e, j, m, k):  # шарнир
    fre = frequency2(k)
    print(fre)
    return ((fre ** 2 / l ** 2) * math.sqrt(e * j / m))


def compute_frequency2(l, e, j, m, k):  # жёсткие опоры
    fre = frequency2(k)
    print(fre)
    return ((fre ** 2 / l ** 2) * math.sqrt(e * j / m))


def compute_frequency3(l, e, j, m, k):  # не жёсткие опоры
    fre = frequency1(k)
    print(fre)
    return (((fre ** 2) / l ** 2) * math.sqrt(e * j / m))


def compute_frequency4(l, e, j, m, k):  # упругое основание
    fre = frequency3(k)
    print(fre)
    return (((fre ** 2) / l ** 2) * math.sqrt(e * j / m))


def krilov_S1(x):
    return 1 / 2 * (math.cosh(x) + math.cos(x))


def krilov_S2(x):
    return 1 / 2 * (math.sinh(x) + math.sin(x))


def krilov_S3(x):
    return 1 / 2 * (math.cosh(x) - math.cos(x))


def krilov_S4(x):
    return 1 / 2 * (math.sinh(x) - math.sin(x))


def compute_table(radiobutton_value, l, e, j):
    res_list = []
    for m in range(1, 11):  # 10 итераций
        res_list.append([])
        # f =lambda l,e,j,m,k:
        for k in range(1, 6):
            if radiobutton_value == 0:
                res_list[-1].append(compute_frequency0(l, e, j, m, k))
            elif radiobutton_value == 1:
                res_list[-1].append(compute_frequency1(l, e, j, m, k))
            elif radiobutton_value == 2:
                res_list[-1].append(compute_frequency2(l, e, j, m, k))
            elif radiobutton_value == 3:
                res_list[-1].append(compute_frequency3(l, e, j, m, k))
    return res_list


def natural_frequency(radiobutton_value, len_sterg, e, j, s, p, colvo=3):
    res_list = []
    m = s * len_sterg * p
    for k in range(1, 1 + colvo):
        print(f"k={k}")
        if radiobutton_value == 0:  # защем
            res_list.append(compute_frequency0(len_sterg, e, j, m, k))
        elif radiobutton_value == 1:  # шарнир
            res_list.append(compute_frequency1(len_sterg, e, j, m, k))
        elif radiobutton_value == 2:  # жёсткие опоры
            res_list.append(compute_frequency2(len_sterg, e, j, m, k))
        elif radiobutton_value == 3:  # не жёсткие опоры
            res_list.append(compute_frequency3(len_sterg, e, j, m, k))
        elif radiobutton_value == 4:  # упругое основание
            res_list.append(compute_frequency4(len_sterg, e, j, m, k))
    print(res_list)
    return res_list


def table_writer(canvas: tkinter.Canvas, res_list: tuple):
    canvas.delete("txt")
    y = 80
    for i in range(len(res_list)):
        x = 110

        for k in range(len(res_list[i])):
            canvas.create_text(x, y, text=str("%.4f" % res_list[i][k]), font="Arial 10", tag="txt")
            x += 70

        y += 33


def compute_a1(p, s, w, e, j):
    if e == 0 or j == 0:  # возникнет деление на ноль
        return None
    ch = p * s * w ** 2
    zn = e * j
    result = (ch / zn) ** (1 / 4)
    if type(result) is complex:
        print("а комплексное")
        return result.real
    return result


def compute_a2(p, s, w, e, j, c0, len_sterg):
    if e == 0 or j == 0:  # возникнет деление на ноль
        return None
    ch = p * s * w ** 2
    zn = e * j
    n0 = c0 * len_sterg ** 4 / zn
    result = (ch / zn - n0) ** (1 / 4)
    if type(result) is complex:
        print("а комплексное")
        return result.real
    return result


def compute_j(d_max, d_min):
    return math.pi / 64 * (d_max ** 4 - d_min ** 4)


def compute_s(d_max, d_min):
    return math.pi / 4 * (d_max ** 2 - d_min ** 2)


def u(x, p, s, w, e, j, c0, cz, len_sterg):
    if cz == 0:
        print("делелие на ноль cz")
        return None
    a = compute_a2(p, s, w, e, j, c0, len_sterg)
    kr4 = krilov_S4(a * len_sterg)
    if kr4 == 0:
        print("деление на 0 kr4")
        return None
    r = e * j * a ** 3 / cz
    slog1 = -krilov_S1(a * x) * r
    slog2 = krilov_S4(a * x)
    slog3 = krilov_S2(a * x) / kr4
    slog4 = r * krilov_S3(a * len_sterg) - krilov_S2(a * len_sterg)
    return slog1 + slog2 + slog3 * slog4


def u_list_0(p, s, w, e, j, len_sterg, shag=0.001) -> (tuple, list) or (None, None):
    result_list = []
    x_list = []
    a = compute_a1(p, s, w, e, j)
    if a is None:  # в а возникает деление на 0
        return None, None
    for x in np.arange(0, len_sterg + shag, shag):
        result_list.append(
            (math.sinh(a * len_sterg) + math.sin(a * len_sterg)) * (math.cosh(a * x) - math.cos(a * x)) - (
                    math.cosh(a * len_sterg) + math.cos(a * len_sterg)) * (math.sinh(a * x) - math.sin(a * x)))
        # result_list.append(
        #     (math.sin(a * len_sterg) - math.sinh(a * len_sterg)) * (math.cosh(a * x) - math.cos(a * x)) - (
        #             math.cosh(a * len_sterg) - math.cos(a * len_sterg)) * (math.sinh(a * x) - math.sin(a * x)))
        x_list.append(x)
    return tuple(x_list), result_list[:]


def u_list_1(p, s, w, e, j, len_sterg, shag=0.001) -> (tuple, list) or (None, None):
    result_list = []
    x_list = []
    # # if not cz:  # при cz=0
    # #     print("делелие на ноль cz")
    # #     return None, None
    a = compute_a1(p, s, w, e, j)
    if a is None:  # в а возникает деление на 0
        return None, None
    # kr4_for_len_sterg = krilov_S4(a * len_sterg)
    # if not kr4_for_len_sterg:  # возникнет деление на ноль
    #     # print("деление на 0 kr4")
    #     return None, None
    # kr2_for_len_sterg = krilov_S2(a * len_sterg)
    # kr3_for_len_sterg = krilov_S3(a * len_sterg)
    # r = e * j * a ** 3 / cz
    for x in np.arange(0, len_sterg + shag, shag):
        #     slog1 = -krilov_S1(a * x) * r
        #     slog2 = krilov_S4(a * x)
        #     slog3 = krilov_S2(a * x) / kr4_for_len_sterg
        #     slog4 = r * kr3_for_len_sterg - kr2_for_len_sterg
        # result_list.append(slog1 + slog2 + slog3 * slog4)
        result_list.append(math.sin(x * a))
        x_list.append(x)
    return tuple(x_list), result_list[:]


def u_list_2(p, s, w, e, j, c0, len_sterg, shag=0.001):
    result_list = []
    x_list = []
    a = compute_a2(p, s, w, e, j, c0, len_sterg)
    if a is None:  # возникает деление на ноль
        return None, None
    for x in np.arange(0, len_sterg + shag, shag):
        result_list.append(krilov_S2(x * a) - krilov_S4(x * a))
        x_list.append(x)
    return x_list, result_list


def u_list_3(p, s, w, e, j, c0, len_sterg, shag=0.001):
    result_list = []
    x_list = []
    a = compute_a2(p, s, w, e, j, c0, len_sterg)
    if a is None:  # возникает деление на ноль
        return None, None
    kr2_for_len_sterg = krilov_S2(a * len_sterg)
    if not kr2_for_len_sterg:  # возникнет деление на ноль
        return None, None
    for x in np.arange(0, len_sterg + shag, shag):
        result_list.append(krilov_S2(a * x) - krilov_S1(a * x) * krilov_S3(a * len_sterg) / kr2_for_len_sterg)
        x_list.append(x)
    return x_list, result_list


def u_list_test(p, s, w, e, j, c0, cz, len_sterg, shag=0.001):
    if cz == 0:
        print("делелие на ноль cz")
        return None
    a = compute_a2(p, s, w, e, j, c0, len_sterg)
    if a is None:  # возникает деление на ноль
        return None, None
    kr4_for_len_sterg = krilov_S4(a * len_sterg)
    if not kr4_for_len_sterg:  # возникнет деление на ноль
        return None, None
    result_list = []
    x_list = []
    r = e * j * a ** 3 / cz
    for x in np.arange(0, len_sterg + shag, shag):
        slog1 = -krilov_S1(a * x) * r
        slog2 = krilov_S4(a * x)
        slog3 = krilov_S2(a * x) / kr4_for_len_sterg
        slog4 = r * krilov_S3(a * len_sterg) - krilov_S2(a * len_sterg)
        result_list.append(slog1 + slog2 + slog3 * slog4)
        if x == 0.5:
            print("значение при x=0.5:", result_list[-1])
        x_list.append(x)
    return x_list, result_list


def paint_grath(animate_check, lx, ly, w, p, time, radiobutton_check):
    lx, ly = np.array(lx), np.array(ly)
    if radiobutton_check == 0:
        title_name = "Защемлённый стержень."
    elif radiobutton_check == 1:
        title_name = "Шарнирно-опёртый стержень."
    elif radiobutton_check == 2:
        title_name = "Шарнирно-опёртый стержень на упругой опоре \n(абсолютно жёсткие опоры)."
    elif radiobutton_check == 3:
        title_name = "Шарнирно-опёртый стержень на упругой опоре \n(абсолютно податливые опоры)."

    if animate_check == 0:  # без анимации
        ly = ly * cm.exp(time * w * complex(0, -1))
        ly = ly.real

        fig = plt.figure("Поперечно-изгибные колебания стержня.")
        plt.title(f"{title_name}\nГрафик отклонения стержня.")

        plt.xlabel("Координаты стержня")
        plt.ylabel("Отклонение стержня")
        plt.plot(lx, ly, label="{}-я секунда w={}".format(time, w))
        plt.grid(True)
        plt.legend()
    else:  # с анимацией
        gridsize = (1, 2)
        if animate_check == 0:
            fig = plt.figure("Стержень закреплён жёстко", figsize=(11, 5))
        else:
            fig = plt.figure("Стержень закреплён не жёстко",
                             figsize=(11, 5))
        camera = Camera(fig)

        ax2 = plt.subplot2grid(gridsize, (0, 1))
        plt.title("Изменение отклонения со временем")
        plt.grid(True)
        plt.xlabel("Координаты стержня")
        plt.ylabel("Отклонение стержня")

        ttt = np.arange(0, 50, 0.5)
        for timer in ttt:
            lyy = ly * cm.exp(timer * w * complex(0, -1))
            lyy = lyy.real
            pl = plt.plot(lx, lyy, color="red")
            plt.legend(pl, ["{}-я секунда m={}".format(timer, p)])
            camera.snap()

        ax1 = plt.subplot2grid(gridsize, (0, 0))
        if animate_check == 0:
            plt.title("Стержень закреплён жёстко\nграфик отклонения стержня".format(time))
        else:
            plt.title("Стержень закреплён не жёстко\nграфик отклонения стержня".format(time))
        plt.xlabel("Координаты стержня")
        plt.ylabel("Отклонение стержня")
        plt.plot(lx, ly, label="{}-я секунда m={}".format(time, p), color="blue")
        plt.grid(True)
        plt.legend()
        anim = camera.animate()

        date = dt.datetime.now().strftime("%d-%m-%Y-%H.%M.%S")
        anim.save("C:/Users/dimon/Pycharm/код/анимация/{}.gif".format(date), writer='imagemagick')
    plt.show()


def paint_grath2(x_list: list, y_list: list, l: list, radiobutton) -> None:
    plt.figure()
    plt.grid()
    plt.xlabel("Координаты стержня")
    plt.ylabel("Амплитуда стержня")
    k = len(l)
    if radiobutton == 0:
        plt.title("Защемлённый стержень")
    elif radiobutton == 1:
        plt.title("Шарнирно-опёртый стержень")
    elif radiobutton == 2:
        plt.title("Шарнирно-опёртый стержень\nЖёсткие опоры")
    elif radiobutton == 3:
        plt.title("Шарнирно-опёртый стержень\nАбсолютно податливые опоры")
    elif radiobutton == 4:
        plt.title("Шарнирно-опёртый стержень\nУпругое основание")
    for i in range(len(l)):
        plt.plot(x_list[i], y_list[i], label=f"Мода {k}")
        # plt.plot(x_list[1], y_list[1], "g-",label=f"k=2 w={l[1]}")
        # plt.plot(x_list[2], y_list[2], "k-.",label=f"k=1 w={l[2]}")
        k -= 1

    plt.legend(loc="lower left")
    plt.show()


# endregion стержня

# region пододольные колебания стержня
def compute_sigma(p, e):
    if e:  # если е ноль, то возникает деление на ноль
        return math.sqrt(p / e)

    else:
        return None


def compute_frequency_for_prodol_sterg1(x, s, e, len_sterg, sig, massa):
    tangens = math.tan(sig * x * len_sterg)
    zn = len_sterg * tangens
    if not zn:  # вознекнет деление на ноль
        raise ZeroDivisionError
    return ((s * sig * e * len_sterg) / zn) - x * massa


def find_zero(x0, x1, sig, s, e, len_sterg, massa, eps=0.0001):
    f_x0 = compute_frequency_for_prodol_sterg1(x0, s, e, len_sterg, sig, massa)
    f_x1 = compute_frequency_for_prodol_sterg1(x1, s, e, len_sterg, sig, massa)
    if f_x0 * f_x1 < 0:
        if f_x0 == 0:
            return x0
        elif f_x1 == 0:
            return x1
        if x1 - x0 <= eps:
            return x1 - eps / 2
        else:
            x_polovina = x0 + (x1 - x0) / 2
            res1 = find_zero(x0, x_polovina, sig, s, e, len_sterg, massa)
            res2 = find_zero(x_polovina, x1, sig, s, e, len_sterg, massa)
            if res1 is not None and res2 is None:
                return res1
            elif res1 is None and res2 is not None:
                return res2
            elif res1 == res2 != None:
                return res1
    else:
        return None


def compute_table_for_prodol_sterg(p, e, s, len_sterg, shag=0.01):
    sig = compute_sigma(p, e)
    if not sig:
        raise ZeroDivisionError
    res_list = []
    for m in range(1, 11):
        x = 0.00001
        res_list.append([])
        while len(res_list[-1]) < 5:
            res = find_zero(x, x + shag, sig, s, e, len_sterg, m)
            if res is not None:
                res_list[-1].append(res)
            x += shag
    return res_list


def compute_frequency_for_prodol_sterg2():
    pass


# endregion

def main1(rad=0):
    len_sterg = 1
    e = 0.89
    j = compute_j(0.12, 0.1)
    s = compute_s(0.12, 0.1)
    p = 7800
    cz = 1 * 10 ** 6
    c0 = 2000

    l = natural_frequency(rad, len_sterg, e, j, s, p)
    l.reverse()
    lx = []
    ly = []
    k = 1
    for i in l:
        if rad == 0:
            # защемлённый
            x, y = u_list_0(p, s, i, e, j, len_sterg)
        elif rad == 1:
            # шарнирно-опёртый
            x, y = u_list_1(p, s, i, e, j, len_sterg)
        elif rad == 2:
            x, y = u_list_2(p, s, i, e, j, c0, len_sterg)
        elif rad == 3:
            x, y = u_list_3(p, s, i, e, j, c0, len_sterg)
        elif rad == 4:
            x, y = u_list_test(p, s, i, e, j, c0, cz, len_sterg)

        lx.append(x)
        ly.append(y)
    paint_grath2(lx, ly, l, rad)


def main2(rad=4):
    len_sterg = 1
    e = 0.89
    j = compute_j(0.12, 0.1)
    s = compute_s(0.12, 0.1)
    p = 7800
    cz = 1 * 10 ** 6
    c0 = 200

    lx, ly = frequency3(p, s, e, j, c0, cz, len_sterg)
    plt.plot(lx, ly)
    plt.show()


def main3():
    len_sterg = 1
    e = 0.89
    # e = 1
    j = compute_j(0.12, 0.1)
    # j = 1
    s = compute_s(0.12, 0.1)
    p = 7800
    cz1 = 100000000
    cz2 = 100000000
    c0 = 2000
    # 2 * shx * sinx + ((x ^ 3 / 1) * 2) * (shx * cosx - sinx * chx) + ((x ^ 3 / 1) ^ 2) * (1 - chx * cosx)
    # 2 * sinh(x) * sin(x) + ((x ^ 3 / 1) * 2) * (sinh(x) * cos(x) - sin(x) * cosh(x)) + ((x ^ 3 / 1) ^ 2) * (1 - cosh(x) * cos(x)) = y
    lx = []
    ly = []

    n1 = (cz1 * len_sterg ** 3) / e * j
    n2 = (cz2 * len_sterg ** 3) / e * j
    shag = 0.0000001
    for x in tqdm(np.arange(0, 5, shag)):
        # la = compute_a2(p, s, x, e, j, c0, len_sterg)  # x частота
        kk1 = x ** 3 / n1
        kk2 = x ** 3 / n2

        slog1 = (kk1 + kk2) * math.sin(x) * math.sinh(x)

        slog2 = (kk1 + kk2) * (math.sinh(x) * math.cos(x) - math.sin(x) * math.cosh(x))

        slog3 = (kk1 * kk2) * (1 - math.cosh(x) * math.cos(x))
        y = slog1 + slog2 + slog3
        lx.append(x)
        ly.append(y)

        if abs(y) <= 0.00001:
            print(f"x={x:.7f} y={y:.7f}")

    plt.grid()
    plt.plot(lx, ly)
    plt.show()


def main4():
    len_sterg = 1
    e = 0.89
    # e = 1
    j = compute_j(0.12, 0.1)
    # j = 1
    s = compute_s(0.12, 0.1)
    p = 7800
    cz1 = 10000000
    cz2 = 10000000
    c0 = 10
    lx = []
    ly = []
    l = natural_frequency(4, len_sterg, e, j, s, p)
    l.reverse()
    print(l)
    for i in l:
        x, y = u_list_test(p, s, i, e, j, c0, cz1, len_sterg)
        lx.append(x)
        ly.append(y)
    paint_grath2(lx, ly, l, 4)


if __name__ == '__main__':
    # main1(0)
    # main2()
    # main3()
    main4()
    # print(krilov_S1(6.7))