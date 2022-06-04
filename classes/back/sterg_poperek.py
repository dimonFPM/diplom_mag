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


def frequency1(k):
    return math.pi / 2 + math.pi * k


def frequency2(k):
    return math.pi * k


def compute_frequency1(l, e, j, m, k):  # защем
    fre = frequency1(k)
    print(fre)
    return (((fre ** 2) / l ** 2) * math.sqrt(e * j / m))


def compute_frequency2(l, e, j, m, k):  # шарнир
    fre = frequency2(k)
    print(fre)
    return ((fre ** 2 / l ** 2) * math.sqrt(e * j / m))


def compute_frequency3(l, e, j, m, k):  # жёсткие опоры
    fre = frequency2(k)
    print(fre)
    return ((fre ** 2 / l ** 2) * math.sqrt(e * j / m))


def compute_frequency4(l, e, j, m, k):  # не жёсткие опоры
    fre = frequency1(k)
    print(fre)
    return (((fre ** 2) / l ** 2) * math.sqrt(e * j / m))


# def compute_(p, s, w, e, j, c0, cz, len_sterg):
#     n = (cz * l ** 3) / e * j
#     la = compute_a2(p, s, w, e, j)
#     n0 = (c0 * len_sterg ** 4) / e * j
#     kk = la ** 3 / n
#     slog1 = 2 * kk * math.sin(la) * math.sinh(la)
#     slog2 = 2 * kk * (math.sinh(la) * math.cos(la) - math.sin(la) * math.cosh(la))
#     slog3 = kk ** 2 * (1 - math.cosh(la) * math.cos(la))
#     return slog1+slog2+slog3


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
                res_list[-1].append(compute_frequency1(l, e, j, m, k))
            elif radiobutton_value == 1:
                res_list[-1].append(compute_frequency2(l, e, j, m, k))
            elif radiobutton_value == 2:
                res_list[-1].append(compute_frequency3(l, e, j, m, k))
            elif radiobutton_value == 3:
                res_list[-1].append(compute_frequency4(l, e, j, m, k))
    return res_list


def natural_frequency(radiobutton_value, len_sterg, e, j, s, p,colvo=3):
    res_list = []
    m = s * len_sterg * p
    for k in range(1, 1+colvo):
        print(f"k={k}")
        if radiobutton_value == 0:
            res_list.append(compute_frequency1(len_sterg, e, j, m, k))
        elif radiobutton_value == 1:
            res_list.append(compute_frequency2(len_sterg, e, j, m, k))
        elif radiobutton_value == 2:
            res_list.append(compute_frequency3(len_sterg, e, j, m, k))
        elif radiobutton_value == 3:
            res_list.append(compute_frequency4(len_sterg, e, j, m, k))
        # elif radiobutton_value == 4:
        #     res_list.append(compute_frequency1(len_sterg, e, j, m, k))
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
    n = c0 * len_sterg ** 4 / zn
    result = (ch / zn - n) ** (1 / 4)
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
        # result_list.append(
        #     (math.sinh(a * len_sterg) + math.sin(a * len_sterg)) * (math.cosh(a * x) - math.cos(a * x)) - (
        #             math.cosh(a * len_sterg) + math.cos(a * len_sterg)) * (math.sinh(a * x) - math.sin(a * x)))
        result_list.append(
            (math.sin(a * len_sterg) - math.sinh(a * len_sterg)) * (math.cosh(a * x) - math.cos(a * x)) - (
                    math.cosh(a * len_sterg) - math.cos(a * len_sterg)) * (math.sinh(a * x) - math.sin(a * x)))
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
        result_list.append(krilov_S2(x*a) - krilov_S4(x*a))
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
            print(result_list[-1])
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
    k=len(l)
    if radiobutton == 0:
        plt.title("Защемлённый стержень")
    elif radiobutton == 1:
        plt.title("Шарнирно-опёртый стержень")
    elif radiobutton == 2:
        plt.title("Шарнирно-опёртый стержень\nЖёсткие опоры")
    elif radiobutton == 3:
        plt.title("Шарнирно-опёртый стержень\nАбсолютно податливые опоры")
    for i in range(len(l)):
        plt.plot(x_list[i], y_list[i], label=f"k={k} w={l[i]}")
        # plt.plot(x_list[1], y_list[1], "g-",label=f"k=2 w={l[1]}")
        # plt.plot(x_list[2], y_list[2], "k-.",label=f"k=1 w={l[2]}")
        k-=1

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

if __name__ == '__main__':

    rad = 4 # 0-3
    len_sterg = 1
    e = 0.89
    j = compute_j(0.12, 0.1)
    s = compute_s(0.12, 0.1)
    p = 7800
    cz = 1 * 10 ** 6
    c0 = 2000

    l = natural_frequency(rad, len_sterg, e, j, s, p)
    l.reverse()
    # exit()  -0.2533596530556679
    # exit()  -0.24569402635097504
    # exit()  -0.2551506981253624
    # exit()  -0.34525705873966217
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
        # elif rad == 4:
        #     x, y = u_list_test(p, s, i, e, j, c0, cz, len_sterg)

        # lx.append(x)
        # ly.append(y)
        # print(lx, "\n", ly)
        # paint_grath(0,x,y,i,p,0,rad)
        plt.grid()
        plt.plot(x, y, label=f"k={k} w={i}")  # i  не правильное
        plt.legend(loc="lower left")
        k += 1
    plt.show()
