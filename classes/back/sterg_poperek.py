import datetime
import tkinter
import datetime as dt
import math
import time
import cmath as cm
import numba
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


def compute_frequency1(l, e, j, m, k):
    return (((math.pi ** 2 * (1 / 4 + k + k ** 2)) / l ** 2) * math.sqrt(e * j / m))


def compute_frequency2(l, e, j, m, k):
    return (((math.pi ** 2 * k ** 2) / l ** 2) * math.sqrt(e * j / m))


def compute_frequency3(l, e, j, m, k):
    return (((math.pi ** 2 * k ** 2) / l ** 2) * math.sqrt(e * j / m))


def compute_frequency4(l, e, j, m, k):
    return (((math.pi ** 2 * (1 / 4 + k + k ** 2)) / l ** 2) * math.sqrt(e * j / m))


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


def table_writer(canvas: tkinter.Canvas, res_list: tuple):
    canvas.delete("txt")
    y = 80
    for i in range(len(res_list)):
        x = 110

        for k in range(len(res_list[i])):
            canvas.create_text(x, y, text=str("%.4f" % res_list[i][k]), font="Arial 10", tag="txt")
            x += 70

        y += 33


def compute_a(p, s, w, e, j, c0, len_sterg):
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
    a = compute_a(p, s, w, e, j, c0, len_sterg)
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


def u_list_1(p, s, w, e, j, c0, cz, len_sterg, shag=0.001) -> (tuple, list) or (None, None):
    result_list = []
    x_list = []
    if not cz:  # при cz=0
        print("делелие на ноль cz")
        return None, None
    a = compute_a(p, s, w, e, j, c0, len_sterg)
    if a is None:  # в а возникает деление на 0
        return None, None
    kr4_for_len_sterg = krilov_S4(a * len_sterg)
    if not kr4_for_len_sterg:  # возникнет деление на ноль
        # print("деление на 0 kr4")
        return None, None
    kr2_for_len_sterg = krilov_S2(a * len_sterg)
    kr3_for_len_sterg = krilov_S3(a * len_sterg)
    r = e * j * a ** 3 / cz
    for x in np.arange(0, len_sterg + shag, shag):
        slog1 = -krilov_S1(a * x) * r
        slog2 = krilov_S4(a * x)
        slog3 = krilov_S2(a * x) / kr4_for_len_sterg
        slog4 = r * kr3_for_len_sterg - kr2_for_len_sterg
        result_list.append(slog1 + slog2 + slog3 * slog4)
        x_list.append(x)
    return tuple(x_list), result_list[:]


def u_list_2(p, s, w, e, j, c0, len_sterg, shag=0.001):
    result_list = []
    x_list = []
    a = compute_a(p, s, w, e, j, c0, len_sterg)
    if a is None:  # возникает деление на ноль
        return None, None
    for x in np.arange(0, len_sterg + shag, shag):
        result_list.append(krilov_S2(a * x) - krilov_S4(a * x))
        x_list.append(x)
    return x_list, result_list


def u_list_3(p, s, w, e, j, c0, len_sterg, shag=0.001):
    result_list = []
    x_list = []
    a = compute_a(p, s, w, e, j, c0, len_sterg)
    if a is None:  # возникает деление на ноль
        return None, None
    kr2_for_len_sterg = krilov_S2(a * len_sterg)
    if not kr2_for_len_sterg:  # возникнет деление на ноль
        return None, None
    for x in np.arange(0, len_sterg + shag, shag):
        result_list.append(krilov_S2(a * x) - krilov_S1(a * x) * krilov_S3(a * len_sterg) / kr2_for_len_sterg)
        x_list.append(x)
    return x_list, result_list


def pain_grath(animate_check, lx, ly, w, upr_koef, time):
    lx, ly = np.array(lx), np.array(ly)
    if animate_check == 0:  # без анимации
        ly = ly * cm.exp(time * w * complex(0, -1))
        ly = ly.real
        if animate_check == 0:
            fig = plt.figure("Стержень закреплён жёстко.")
            plt.title("Стержень закреплён жёстко.\nГрафик отклонения стержня.".format(time))
        elif animate_check == 1:
            fig = plt.figure(
                "Стержень закреплён не жёстко.")
            plt.title("Стержень закреплён не жёстко.\nГрафик отклонения стержня.".format(
                time))
        elif animate_check == 2:
            pass
        elif animate_check == 3:
            pass

        plt.xlabel("Координаты стержня")
        plt.ylabel("Отклонение стержня")
        plt.plot(lx, ly, label="{}-я секунда m={}".format(time, upr_koef))
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
            plt.legend(pl, ["{}-я секунда m={}".format(timer, upr_koef)])
            camera.snap()

        ax1 = plt.subplot2grid(gridsize, (0, 0))
        if animate_check == 0:
            plt.title("Стержень закреплён жёстко\nграфик отклонения стержня".format(time))
        else:
            plt.title("Стержень закреплён не жёстко\nграфик отклонения стержня".format(time))
        plt.xlabel("Координаты стержня")
        plt.ylabel("Отклонение стержня")
        plt.plot(lx, ly, label="{}-я секунда m={}".format(time, upr_koef), color="blue")
        plt.grid(True)
        plt.legend()
        anim = camera.animate()

        date = dt.datetime.now().strftime("%d-%m-%Y-%H.%M.%S")
        anim.save("C:/Users/dimon/Pycharm/код/анимация/{}.gif".format(date), writer='imagemagick')
    plt.show()


# endregion стержня
# region пододольные колебания стержня
def compute_sigma(p, e):
    if e:  # если е ноль, то возникает деление на ноль
        return math.sqrt(p / e)
    else:
        return None


def compute_frequency_for_prodol_sterg1(x, s, p, e, len_sterg, sig, massa):
    tangens = math.tan(sig * x)
    if not tangens:  # вознекнет деление на ноль
        raise ZeroDivisionError
    return ((s * sig * e * len_sterg) / (len_sterg * math.tan(sig * x * len_sterg))) - x * massa


def find_zero(x0, x1, sig, count_zeros, s, e, len_sterg, massa, eps=0.0001):
    f_x0 = compute_frequency_for_prodol_sterg1(x0, s, e, len_sterg, sig, massa)
    f_x1 = compute_frequency_for_prodol_sterg1(x1, s, e, len_sterg, sig, massa)
    if f_x0 * f_x1 < 0:
        if x1 - x0 <= eps:
            return x1 - eps / 2
        else:
            if x0 * x_polovina < 0:

            elif x_polovina * x1 < 0:
                pass

    x0 = x1
    x1 = x0 + shag
    x_polovina = x0 + shag / 2
    # if len(res_list)==count_zeros:
    #     pass


def compute_table_for_prodol_sterg(p, e, len_sterg, sig, masssa, shag=0.01):
    sig = compute_sigma(p, e)
    x = 0
    if not sig:
        raise ZeroDivisionError
    res_list = []
    for m in range(1, 11):
        res_list.append([])
        while len(res_list[-1]) < 5:
            res = find_zero()
            if res is not None:
                res_list[-1].append(res)
            x += shag


def compute_frequency_for_prodol_sterg2():
    pass


# endregion

if __name__ == '__main__':
    s = compute_s(0.12, 0.1)
    j = compute_j(0.12, 0.1)
    t = datetime.datetime.now
    #              x, p,    s,                 w, e,    j, c0, cz,         len_sterg
    # print("res=", u_list(7800, s, 5, 0.89, j, 0.2 * 10 ** 3, 1 * 10 ** 6, 1))
    lx, ly = u_list_1(1, compute_s(0.12, 0.1), 1, 1, compute_j(0.12, 0.1), 1, 1, 1)
    pain_grath(0, lx, ly, 1, 1, 1)
    print(datetime.datetime.now() - t)
    pass
