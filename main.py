import cmath as cm
import datetime as dt
import math as math
import tkinter
from tkinter import *
from tkinter import messagebox as mbox

from fontTools.ttLib.tables._k_e_r_n import table__k_e_r_n

import classes.back.sterg_poperek as bspi
import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera

root = Tk()
root.title("Моделирование")
root.geometry("270x100+100+100")
root.resizable(False, False)


def balka():
    root1 = Toplevel()
    root1.title("Моделирование фундамента")
    root1.geometry("730x560+310+20")
    root1.resizable(False, False)

    def clean():  # обработчик кнопки очистка
        e_e.delete(0, END)
        j_e.delete(0, END)
        m_e.delete(0, END)
        w_e.delete(0, END)
        t_e.delete(0, END)
        k_e.delete(0, END)
        a_e.delete(0, END)
        r_var.set(0)
        r_var1.set(0)
        q1.delete("txt")
        # pass

    def f(x):
        s = r_var.get()
        if s == 1:
            return math.cos(x)
        elif (s == 0) or (s == 2):
            return math.tan(x) + math.tanh(x)

    def v2(x, y):
        s = (f(y) - f(x)) / (y - x)
        return s

    def v3(y0, y1, y2):
        s = (v2(y1, y2) - v2(y0, y1)) / (y2 - y0)
        return s

    def find(eps, x0, x1, x2):
        s = f(x0)
        s1 = f(x2)
        while True:
            w = v2(x1, x2) + (x2 - x1) * v3(x0, x1, x2)
            if s > s1:
                xn = x2 - (2 * f(x2)) / (w - math.sqrt(w * w - 4 * f(x2) * v3(x0, x1, x2)))
            elif s < s1:
                xn = x2 - (2 * f(x2)) / (w + math.sqrt(w * w - 4 * f(x2) * v3(x0, x1, x2)))
            if (abs(xn - x2) < eps) and (f(xn) < eps):
                return xn
            x0 = x1
            x1 = x2
            x2 = xn

    def tableBalka():  # обработчик кнопки рассчитать
        s = r_var.get()  # граниное условие
        s1 = r_var1.get()  # вид нагрузки
        eps = float(t_e.get())  # точность
        shag = 0.00001
        x = 110
        q1.delete("txt")
        global l
        global lx
        global ly
        l = list(l)
        ly = list(ly)
        lx.clear()
        ly.clear()
        l.clear()
        check = 0
        try:
            a_2 = float(a_e.get())  # полуширина балки
            if s != 1:  # заполнение таблицы
                for j in range(5):
                    i = 0
                    gr = 0
                    y = 80
                    sc = False
                    while i < 10:
                        if f(gr) * f(gr + shag) < 0:
                            if sc == True:
                                v = find(0.0001, gr, gr + shag / 2, gr + shag) / (j + 1)
                                v = float("{0:.3f}".format(v))
                                q1.create_text(x, y, text=str(v), font="Arial 10", tag="txt")
                                i += 1
                                y += 33
                                sc = False
                            else:
                                sc = True
                        gr += shag
                    x += 70
                gr = 0
                y = 80
                i = 0
                sc = False
                while i < 100:  # заполнение списка
                    if f(gr) * f(gr + shag) < 0:
                        if sc == True:
                            v = find(0.0001, gr, gr + shag / 2, gr + shag) / a_2  #
                            v = float("{0:.3f}".format(v))
                            l.append(v)
                            if i < 10:
                                q1.create_text(455, y, text=str(v), font="Arial 10", tag="txt")
                                y += 33
                            i += 1
                            sc = False
                        else:
                            sc = True
                    gr += shag
            elif s == 1:  # заполнение таблицы
                for j in range(5):
                    i = 0
                    gr = 0
                    y = 80
                    while i < 10:
                        if f(gr) * f(gr + shag) < 0:
                            v = find(0.0001, gr, gr + shag / 2, gr + shag) / (j + 1)
                            v = float("{0:.3f}".format(v))
                            q1.create_text(x, y, text=str(v), font="Arial 10", tag="txt")
                            i += 1
                            y += 33
                        gr += shag
                    x += 70
                gr = 0
                y = 80
                i = 0
                while i < 100:  # заполнение списка
                    if f(gr) * f(gr + shag) < 0:
                        v = find(0.0001, gr, gr + shag / 2, gr + shag) / a_2  #
                        v = float("{0:.3f}".format(v))
                        l.append(v)
                        if i < 10:
                            q1.create_text(455, y, text=str(v), font="Arial 10", tag="txt")
                            y += 33
                        i += 1
                    gr += shag
            if s == 1:  # шарнирное опирание краёв балки
                x = 0
                if s1 == 0:  # первое граничное
                    while x <= a_2:
                        sm = 0
                        size_tec = 0
                        size_pr = 0
                        lx.append(x)
                        for k in range(100):
                            size_pr = size_tec
                            ch = ((-1) ** (k + 2)) * math.cos(x * l[k])
                            zn = ((float(e_e.get()) * float(j_e.get()) * l[k] ** 4) - (
                                    float(m_e.get()) * float(w_e.get()) ** 2) + float(k_e.get())) * l[k]
                            size_tec = ch / zn
                            if abs(size_tec - size_pr) < eps:
                                break
                            sm += ch / zn
                        else:
                            print("заданная точность не достигнута,увеличьте количество членов ряда")
                        sm = sm * 2 / a_2
                        ly.append(sm)
                        x += a_2 / 1000

                    ly = np.array(ly)
                    # анимация
                    if r_var2.get() == 1:
                        lyy = ly  # сохранение ly для нулевого временного параметра

                    ly = ly * cm.exp(float(time_e.get()) * float(w_e.get()) * complex(0, -1))
                    ly = ly.real

                elif s1 == 1:  # второе граничное
                    while x <= a_2:
                        sm = 0
                        size_tec = 0
                        size_pr = 0
                        lx.append(x)
                        for k in range(100):
                            size_pr = size_tec
                            ch = ((-1) ** (k + 2)) * ((a_2 ** 2) * (l[k] ** 2) - 2) * math.cos(x * l[k])
                            zn = ((float(e_e.get()) * float(j_e.get()) * l[k] ** 4) - (
                                    float(m_e.get()) * float(w_e.get()) ** 2) + float(k_e.get())) * l[k] ** 3
                            size_tec = ch / zn
                            if abs(size_tec - size_pr) < eps:
                                break
                            sm += ch / zn
                        else:
                            print("заданная точность не достигнута,увеличьте количество членов ряда")
                        sm = sm * 2 / a_2
                        ly.append(sm)
                        x += a_2 / 1000

                    ly = np.array(ly)
                    # анимация
                    if r_var2.get() == 1:
                        lyy = ly  # сохранение ly для нулевого временного параметра

                    ly = ly * cm.exp(float(time_e.get()) * float(w_e.get()) * complex(0, -1))
                    ly = ly.real

            elif s == 0:  # жёсткая заделка краёв балки
                x = 0
                if s1 == 0:  # первое граничное
                    while x <= a_2:
                        sm = 0
                        size_tec = 0
                        size_pr = 0
                        lx.append(x)
                        for k in range(100):
                            size_pr = size_tec
                            ch = (math.tanh(a_2 * l[k]) / l[k]) * (
                                    math.cosh(x * l[k]) / math.cosh(a_2 * l[k]) - math.cos(x * l[k]) / math.cos(
                                a_2 * l[k]))
                            zn = ((float(e_e.get()) * float(j_e.get()) * l[k] ** 4) - (
                                    float(m_e.get()) * float(w_e.get()) ** 2) + float(k_e.get())) * (
                                         a_2 / ((math.cosh(a_2 * l[k])) ** 2) + a_2 / ((math.cos(
                                     a_2 * l[k])) ** 2))
                            size_tec = ch / zn
                            if abs(size_tec - size_pr) < eps:
                                break
                            sm += ch / zn
                        else:
                            print("заданная точность не достигнута,увеличьте количество членов ряда")
                        ly.append(sm)
                        x += a_2 / 1000

                    ly = np.array(ly)
                    # анимация
                    if r_var2.get() == 1:
                        lyy = ly  # сохранение ly для нулевого временного параметра

                    ly = ly * cm.exp(float(time_e.get()) * float(w_e.get()) * complex(0, -1))
                    ly = ly.real

                elif s1 == 1:  # второе граничное
                    while x <= a_2:
                        sm = 0
                        size_tec = 0
                        size_pr = 0
                        lx.append(x)
                        for k in range(100):
                            size_pr = size_tec
                            ch = ((-8 * a_2 / l[k] ** 2) + (4 * a_2 ** 2 * math.tanh(a_2 * l[k]) / l[k])) * (
                                    math.cosh(x * l[k]) / math.cosh(a_2 * l[k]) - math.cos(x * l[k]) / math.cos(
                                a_2 * l[k]))
                            zn = ((float(e_e.get()) * float(j_e.get()) * l[k] ** 4) - (
                                    float(m_e.get()) * float(w_e.get()) ** 2) + float(k_e.get())) * (
                                         a_2 / ((math.cosh(a_2 * l[k])) ** 2) + a_2 / ((math.cos(
                                     a_2 * l[k])) ** 2))
                            size_tec = ch / zn
                            if abs(size_tec - size_pr) < eps:
                                break
                            sm += ch / zn
                        else:
                            print("заданная точность не достигнута,увеличьте количество членов ряда")
                        ly.append(sm)
                        x += a_2 / 1000

                    ly = np.array(ly)
                    # анимация
                    if r_var2.get() == 1:
                        lyy = ly  # сохранение ly для нулевого временного параметра

                    ly = ly * cm.exp(float(time_e.get()) * float(w_e.get()) * complex(0, -1))
                    ly = ly.real

            elif s == 2:  # свободное операние
                x = 0
                if s1 == 0:  # равномерно распределённая нагрузка
                    while x <= a_2:
                        sm = 0
                        size_tec = 0
                        size_pr = 0
                        lx.append(x)
                        for k in range(100):
                            size_pr = size_tec
                            ch = 1
                            zn = float(k_e.get()) - float(m_e.get()) * float(w_e.get()) ** 2
                            size_tec = ch / zn
                            if abs(size_tec - size_pr) < eps:
                                break
                            sm += ch / zn
                        else:
                            print("заданная точность не достигнута,увеличьте количество членов ряда")
                        ly.append(sm)
                        x += a_2 / 1000

                    ly = np.array(ly)
                    # анимация
                    if r_var2.get() == 1:
                        lyy = ly  # сохранение ly для нулевого временного параметра

                    ly = ly * cm.exp(float(time_e.get()) * float(w_e.get()) * complex(0, -1))
                    ly = ly.real

                elif s1 == 1:  # параболически распределённая нагрузка
                    while x <= a_2:
                        sm = 0
                        size_tec = 0
                        size_pr = 0
                        lx.append(x)
                        for k in range(100):
                            size_pr = size_tec
                            ch = ((8 / (l[k] ** 3)) * (math.tanh(l[k] * a_2))) * (
                                (math.cosh(l[k] * x) / math.cosh(l[k] * a_2) + math.cos(l[k] * x) / math.cos(
                                    l[k] * a_2)))
                            zn = ((float(e_e.get()) * float(j_e.get()) * l[k] ** 4) - (
                                    float(m_e.get()) * float(w_e.get()) ** 2) + float(k_e.get())) * (
                                         a_2 / ((math.cosh(a_2 * l[k])) ** 2) + a_2 / ((math.cos(a_2 * l[k])) ** 2))
                            size_tec = ch / zn
                            if abs(size_tec - size_pr) < eps:
                                break
                            sm += ch / zn
                        else:
                            print("заданная точность не достигнута,увеличьте количество членов ряда")
                        sm = sm + (a_2 ** 2) / (3 * (float(k_e.get()) - float(m_e.get()) * float(w_e.get())))
                        ly.append(sm)
                        x += a_2 / 1000

                    ly = np.array(ly)
                    # анимация
                    if r_var2.get() == 1:
                        lyy = ly  # сохранение ly для нулевого временного параметра

                    ly = ly * cm.exp(float(time_e.get()) * float(w_e.get()) * complex(0, -1))
                    ly = ly.real
        except ZeroDivisionError:
            check = 1
            mbox.showerror("Ошибка", "Происходит деление на ноль")

        if check == 0:  # отрисовка графиков
            if s == 1:
                titleFig = "Шарнирное опирание краёв балки."
                if s1 == 0:
                    titleGrafik = "Шарнирное опирание краёв балки.\nРавномерно распределённая нагрузка."
                elif s1 == 1:
                    titleGrafik = "Шарнирное опирание краёв балки.\nПараблически распределённая нагрузка."
            elif s == 0:
                titleFig = "Жёсткая заделка краёв балки."
                if s1 == 0:
                    titleGrafik = "Жёсткая заделка краёв балки.\nРавномерно распределённая нагрузка."
                elif s1 == 1:
                    titleGrafik = "Жёсткая заделка краёв балки.\nПараболически распределённая нагрузка."
            elif s == 2:
                titleFig = "Свободное операние балки."
                if s1 == 0:
                    titleGrafik = "Свободное операние балки.\nРавномерно распределённая нагрузка."
                elif s1 == 1:
                    titleGrafik = "Свободное операние балки.\nПараболически распределённая нагрузка."
            if r_var2.get() == 0:  # без анимации
                fig = plt.figure(titleFig)
                plt.title(titleGrafik)
                plt.grid(True)
                plt.xlabel("Координаты точек фундамента")
                plt.ylabel("Вертикальное смещение")
                plt.plot(lx, ly, label="a={} w={} k={}".format(a_2, float(w_e.get()), float(k_e.get())))
                plt.legend()

            else:  # с анимацией
                gridsize = (1, 2)
                fig = plt.figure(titleFig, figsize=(11, 5))
                camera = Camera(fig)
                ax1 = plt.subplot2grid(gridsize, (0, 1))
                plt.title("Изменения смещения со временем.")
                plt.grid(True)
                plt.xlabel("Координаты точек фундамента")
                plt.ylabel("Вертикальное смещение")

                ttt = np.arange(0, 50, 0.5)
                w = float(w_e.get())
                for timer in ttt:
                    ly2 = lyy * cm.exp(timer * w * complex(0, -1))
                    ly2 = ly2.real
                    pl = plt.plot(lx, ly2, color="red")
                    plt.legend(pl, ["{}сек".format(timer)])
                    camera.snap()

                ax2 = plt.subplot2grid(gridsize, (0, 0))
                plt.title(titleGrafik)
                plt.grid(True)
                plt.xlabel("Координаты точек фундамента")
                plt.ylabel("Вертикальное смещение")
                plt.plot(lx, ly, color="blue", label="a={} w={} k={}".format(a_2, float(w_e.get()), float(k_e.get())))
                plt.legend()
                anim = camera.animate()
                date = dt.datetime.now().strftime("%d-%m-%Y-%H.%M.%S")
                anim.save("C:/Users/dimon/Pycharm/код/анимация/{}.gif".format(date), writer='imagemagick')
            plt.show()

    # Canvas
    q1 = Canvas(root1, width=495, height=400, bg="white")
    q1.grid(row=0, column=0, rowspan=8, columnspan=10)
    q1.create_rectangle(2, 2, 496, 401)
    q1.create_rectangle(10, 30, 489, 391)
    q1.create_text(239, 15, text="Зависимость собственных частот от полуширины балки", )
    q1.create_text(40, 45, text="K,a", font="Arial 15")
    q1.create_text(455, 45, text="a", font="Arial 15")
    x = 78.42
    for i in range(7):
        q1.create_line(x, 30, x, 391)
        x += 68.42
    x = 62.81
    for i in range(10):
        q1.create_line(10, x, 489, x)
        x += 32.81
    x = 110
    for i in range(5):
        a = str(i + 1)
        q1.create_text(x, 45, text=a, font="Arial 15")
        x += 70
    x = 80
    for i in range(10):
        a = str(i + 1)
        q1.create_text(40, x, text=a, font="Arial 15")
        x += 33

    # Label
    l1 = Label(root1, text="Входные данные:", font="Arial 15")
    l1.grid(row=8, column=0, columnspan=8, sticky=W)
    l2 = Label(root1, text="Граничные условия:", font="Arial 15")
    l2.grid(row=0, column=10, columnspan=3, sticky=W)
    l3 = Label(root1, text="Вид нагрузки:", font="Arial 15")
    l3.grid(row=4, column=10, columnspan=3, sticky=W)
    e_l = Label(root1, text="E=")
    j_l = Label(root1, text="J=")
    m_l = Label(root1, text="m=")
    w_l = Label(root1, text="w=")
    t_l = Label(root1, text="точность=")
    k_l = Label(root1, text="k=")
    a_l = Label(root1, text="a=")
    time_l = Label(root1, text="время=")
    e_l.grid(row=9, column=0, sticky=W)
    j_l.grid(row=10, column=0, sticky=W)
    m_l.grid(row=11, column=0, sticky=W)
    w_l.grid(row=12, column=0, sticky=W)
    t_l.grid(row=13, column=0, sticky=W)
    k_l.grid(row=9, column=4, sticky=W)
    a_l.grid(row=10, column=4, sticky=W)
    time_l.grid(row=11, column=4, sticky=W)

    # Entry
    e_e = Entry(root1, )
    j_e = Entry(root1, )
    m_e = Entry(root1, )
    w_e = Entry(root1, )
    t_e = Entry(root1, )
    k_e = Entry(root1, )
    a_e = Entry(root1, )
    time_e = Entry(root1, )
    e_e.grid(row=9, column=1, columnspan=2)
    j_e.grid(row=10, column=1, columnspan=2)
    m_e.grid(row=11, column=1, columnspan=2)
    w_e.grid(row=12, column=1, columnspan=2)
    t_e.grid(row=13, column=1, columnspan=2)
    k_e.grid(row=9, column=5, columnspan=2)
    a_e.grid(row=10, column=5, columnspan=2)
    time_e.grid(row=11, column=5, columnspan=2)

    # Button
    b1 = Button(root1, text="Рассчитать", bg="orange", command=tableBalka)
    b1.grid(row=13, column=11)
    b2 = Button(root1, text="Очистить", command=clean, bd=0)
    b2.grid(row=13, column=10)

    # Radiobutton
    r_var = IntVar()
    r_var1 = IntVar()
    r_var1.set(0)
    r_var.set(0)
    r_1 = Radiobutton(root1, text="Жёсткая заделка краёв балки", variable=r_var, value=0)
    r_2 = Radiobutton(root1, text="Шарнирное опирание краёв балки", variable=r_var, value=1)
    r_3 = Radiobutton(root1, text="Свобоное операние балки", variable=r_var, value=2)
    r_4 = Radiobutton(root1, text="Равномерно распределённая\nнагрузка", variable=r_var1, value=0)
    r_5 = Radiobutton(root1, text="Параболически распределённая\nнагрузка", variable=r_var1, value=1)
    r_1.grid(row=1, column=10, columnspan=3, sticky=W)
    r_2.grid(row=2, column=10, columnspan=3, sticky=W)
    r_3.grid(row=3, column=10, columnspan=3, sticky=W)
    r_4.grid(row=5, column=10, columnspan=3, sticky=W)
    r_5.grid(row=6, column=10, columnspan=3, sticky=W)

    # checkbutton
    r_var2 = IntVar()
    r_var2.set(0)
    ch1 = Checkbutton(root1, text="Анимация", variable=r_var2, onvalue=1, offvalue=0)
    ch1.grid(row=9, column=10, sticky=W)

    root1.mainloop()


def sterg():
    root2 = Toplevel()
    root2.title("Моделирование продольных колебаний стержня")
    root2.geometry("700x560+310+20")
    root2.resizable(False, False)

    def clean():  # обработчик кнопки очистка
        e_e.delete(0, END)
        f_e.delete(0, END)
        m_e.delete(0, END)
        w_e.delete(0, END)
        p_e.delete(0, END)
        s_e.delete(0, END)
        l_e.delete(0, END)
        time_e.delete(0, END)
        ny_e.delete(0, END)
        a_e.delete(0, END)
        h_e.delete(0, END)
        r_var.set(0)
        q1.delete("txt")

    def f(x):
        ss = r_var.get()
        s = float(s_e.get())
        p = float(p_e.get())
        e = float(e_e.get())
        sig = math.sqrt(p / e)
        ll = float(l_e.get())
        ny = float(ny_e.get())
        a = float(a_e.get())
        a = a / 2
        h = float(h_e.get())
        global mi
        if ss == 0 and math.tan(sig * x) != 0:
            return ((s * sig * e * ll) / (ll * math.tan(sig * x * ll))) - x * mi
        elif ss == 1:
            q = 2 * x * a * math.sqrt(p * ny / e) * (
                    math.cos(2 * h * x * math.sqrt(p * ny / e)) / math.sin(2 * h * x * math.sqrt(p * ny / e)))
            return e * x * sig * (q - x * x * mi) * math.cos(x * sig * ll) - x * x * (
                    mi * q + e * e * sig) * math.sin(
                x * sig * ll)

    def v2(x, y):
        s = (f(y) - f(x)) / (y - x)
        return s

    def v3(y0, y1, y2):
        s = (v2(y1, y2) - v2(y0, y1)) / (y2 - y0)
        return s

    def find(eps, x0, x1, x2):
        s = f(x0)
        s1 = f(x2)
        while True:
            w = v2(x1, x2) + (x2 - x1) * v3(x0, x1, x2)
            if s > s1:
                xn = x2 - (2 * f(x2)) / (w - math.sqrt(w * w - 4 * f(x2) * v3(x0, x1, x2)))
            elif s < s1:
                xn = x2 - (2 * f(x2)) / (w + math.sqrt(w * w - 4 * f(x2) * v3(x0, x1, x2)))
            if (abs(xn - x2) < eps) and (f(xn) < eps):
                return xn
            x0 = x1
            x1 = x2
            x2 = xn

    #####################################################

    def tableSterg():
        global l
        global lx
        global ly
        global mi  ###################################
        l = list(l)
        ly = list(ly)
        lx.clear()
        ly.clear()
        l.clear()
        q1.delete("txt")
        ff = float(f_e.get())
        w = float(w_e.get())
        p = float(p_e.get())
        e = float(e_e.get())
        s = float(s_e.get())
        ll = float(l_e.get())
        mm = float(m_e.get())
        time = float(time_e.get())
        ny = float(ny_e.get())
        a = float(a_e.get())
        a = a / 2
        h = float(h_e.get())
        ss = r_var.get()
        lx = list(np.linspace(0, ll, 1000))
        ly = np.zeros(1000)
        cheek = 0
        ####заполнение таблицы
        shag = 0.00001
        y = 80
        for i in range(1, 11, 1):
            mi = i
            x = 110
            xx = shag
            if ss == 0:
                sc = True
            else:
                sc = False
            while len(l) < 6:
                if f(xx) * f(xx + shag) < 0:
                    if sc == True:
                        v = find(0.0001, xx, xx + shag / 2, xx + shag)
                        v = float("{0:.5f}".format(v))
                        q1.create_text(x, y, text=str(v), font="Arial 10", tag="txt")
                        x += 70
                        sc = False
                    else:
                        sc = True
                xx += shag
            y += 33
        ######################
        if ss == 0:
            try:
                zn = (w * s * math.sqrt(e * p) * math.cos(w * ll * math.sqrt(p / e))) - (
                        w * w * mm * math.sin(w * ll * math.sqrt(p / e)))
                for i in range(len(lx)):
                    ch = ff * math.sin(w * lx[i] * math.sqrt(p / e))
                    ly[i] = ch / zn
                # анимация
                if r_var1.get() == 1:
                    lyy = ly

                ly = ly * cm.exp(time * w * complex(0, -1))
                ly = ly.real
            except ValueError:
                mbox.showerror("Ошибка", "Отрицательное число под корнем")
                cheek += 1
            except ZeroDivisionError:
                mbox.showerror("Ошибка", "Происходит деление на ноль")
                cheek += 1

        else:
            try:
                ct = math.cos(h * w * math.sqrt(p * (e / (2 * (1 - ny))) / ((1 - 2 * ny) / (2 - 2 * ny)))) / math.sin(
                    h * w * math.sqrt(p * (e / (2 * (1 - ny))) / ((1 - 2 * ny) / (2 - 2 * ny))))
                q = 2 * w * a * math.sqrt(p * (e / (2 * (1 - ny))) / ((1 - 2 * ny) / (2 - 2 * ny))) * ct
                sig = math.sqrt(p / e)
                zn = e * w * sig * (q - w * w * mm) * math.cos(w * sig * ll) - w * w * (
                        mm * q + e * e * sig * sig) * math.sin(
                    w * sig * ll)
                for i in range(len(lx)):
                    ch = ff * (e * w * sig * math.cos(w * sig * lx[i]) + q * math.sin(w * sig * lx[i]))
                    ly[i] = ch / zn
                # анимация
                if r_var1.get() == 1:
                    lyy = ly

                ly = ly * cm.exp(time * w * complex(0, -1))
                ly = ly.real
            except ValueError:
                mbox.showerror("Ошибка", "Отрицательное число под корнем")
                cheek += 1
            except ZeroDivisionError:
                mbox.showerror("Ошибка", "Происходит деление на ноль")
                cheek += 1

        # отрисовка графика
        if cheek == 0:
            if r_var1.get() == 0:  # без анимации
                if ss == 0:
                    fig = plt.figure("Стержень закреплён жёстко.")
                    plt.title("Стержень закреплён жёстко.\nГрафик отклонения стержня.".format(time))
                else:
                    fig = plt.figure(
                        "Стержень закреплён не жёстко.")
                    plt.title("Стержень закреплён не жёстко.\nГрафик отклонения стержня.".format(
                        time))

                plt.xlabel("Координаты стержня")
                plt.ylabel("Отклонение стержня")
                plt.plot(lx, ly, label="{}-я секунда m={}".format(time, mm))
                plt.grid(True)
                plt.legend()
            else:  # с анимацией
                gridsize = (1, 2)
                if ss == 0:
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
                    ly2 = lyy * cm.exp(timer * w * complex(0, -1))
                    ly2 = ly2.real
                    pl = plt.plot(lx, ly2, color="red")
                    plt.legend(pl, ["{}-я секунда m={}".format(timer, mm)])
                    camera.snap()

                ax1 = plt.subplot2grid(gridsize, (0, 0))
                if ss == 0:
                    plt.title("Стержень закреплён жёстко\nграфик отклонения стержня".format(time))
                else:
                    plt.title("Стержень закреплён не жёстко\nграфик отклонения стержня".format(time))
                plt.xlabel("Координаты стержня")
                plt.ylabel("Отклонение стержня")
                plt.plot(lx, ly, label="{}-я секунда m={}".format(time, mm), color="blue")
                plt.grid(True)
                plt.legend()
                anim = camera.animate()

                date = dt.datetime.now().strftime("%d-%m-%Y-%H.%M.%S")
                anim.save("C:/Users/dimon/Pycharm/код/анимация/{}.gif".format(date), writer='imagemagick')
        plt.show()

    ###отрисовка интерфеса данного окна
    q1 = Canvas(root2, width=430, height=400, bg="white")
    q1.grid(row=0, column=0, rowspan=8, columnspan=10)
    q1.create_rectangle(2, 2, 431, 401)
    q1.create_rectangle(10, 30, 420.58, 391)
    q1.create_text(239, 15, text="Зависимость собственных частот от массы тела")
    q1.create_text(40, 45, text="m,w", font="Arial 15")
    x = 78.42
    for i in range(6):
        q1.create_line(x, 30, x, 391)
        x += 68.42
    x = 62.81
    for i in range(10):
        q1.create_line(10, x, 420.58, x)
        x += 32.81
    x = 110
    for i in range(5):
        a = str(i + 1)
        q1.create_text(x, 45, text=a, font="Arial 15")
        x += 70
    x = 80
    for i in range(10):
        a = str(i + 1)
        q1.create_text(40, x, text=a, font="Arial 15")
        x += 33

    # Label
    l1 = Label(root2, text="Входные данные:", font="Arial 15")
    l1.grid(row=8, column=0, columnspan=8, sticky=W)
    l2 = Label(root2, text="Граничные условия:", font="Arial 15")
    l2.grid(row=0, column=10, columnspan=3, sticky=W)
    l3 = Label(root2, text="Дополнительные данные:", font="Arial 15")
    l3.grid(row=4, column=10, columnspan=3, sticky=SW)

    e_l = Label(root2, text="E=")
    f_l = Label(root2, text="F=")
    m_l = Label(root2, text="m=")
    w_l = Label(root2, text="w=")
    t_l = Label(root2, text="точность=")
    p_l = Label(root2, text="p=")
    s_l = Label(root2, text="s=")
    l_l = Label(root2, text="l=")
    time_l = Label(root2, text="время=")
    ny_l = Label(root2, text="Коэф. Пуассона=")
    h_l = Label(root2, text="Ширина упругой полосы=")
    a_l = Label(root2, text="Ширина стержня=")

    e_l.grid(row=9, column=0, sticky=W)
    f_l.grid(row=10, column=0, sticky=W)
    m_l.grid(row=11, column=0, sticky=W)
    w_l.grid(row=12, column=0, sticky=W)

    p_l.grid(row=9, column=4, sticky=W)
    s_l.grid(row=10, column=4, sticky=W)
    l_l.grid(row=11, column=4, sticky=W)
    time_l.grid(row=12, column=4, sticky=W)
    ny_l.grid(row=5, column=10, sticky=NW)
    h_l.grid(row=6, column=10, sticky=NW)
    a_l.grid(row=7, column=10, sticky=NW)

    # Entry
    e_e = Entry(root2)
    f_e = Entry(root2)
    m_e = Entry(root2)
    w_e = Entry(root2)

    p_e = Entry(root2)
    s_e = Entry(root2)
    l_e = Entry(root2)
    time_e = Entry(root2)
    ny_e = Entry(root2, width=15)
    h_e = Entry(root2, width=15)
    a_e = Entry(root2, width=15)

    e_e.grid(row=9, column=1, columnspan=2)
    f_e.grid(row=10, column=1, columnspan=2)
    m_e.grid(row=11, column=1, columnspan=2)
    w_e.grid(row=12, column=1, columnspan=2)
    p_e.grid(row=9, column=5, columnspan=2)
    s_e.grid(row=10, column=5, columnspan=2)
    l_e.grid(row=11, column=5, columnspan=2)
    time_e.grid(row=12, column=5, columnspan=2)
    ny_e.grid(row=5, column=11, sticky=NW)
    h_e.grid(row=6, column=11, sticky=NW)
    a_e.grid(row=7, column=11, sticky=NW)

    # Button
    b1 = Button(root2, text="Рассчитать", bg="orange", command=tableSterg)
    b1.grid(row=13, column=11)
    b2 = Button(root2, text="Очистить", bd=0, command=clean)
    b2.grid(row=13, column=10)

    # Radiobutton
    r_var = IntVar()
    r_var.set(0)
    r_1 = Radiobutton(root2, text="Стержень закреплён жёстко", variable=r_var, value=0)
    r_2 = Radiobutton(root2,
                      text="Стержень без трения контактирует с\nполуограниченным деформируемым\nоснованием средой"
                           "\n(Необходимы дополнительные данные)",
                      variable=r_var, value=1)
    r_1.grid(row=1, column=10, columnspan=3, sticky=W)
    r_2.grid(row=2, column=10, columnspan=3, sticky=W)

    # checkbutton
    r_var1 = IntVar()
    r_var1.set(0)
    ch1 = Checkbutton(root2, text="Анимация", variable=r_var1, onvalue=1, offvalue=0)
    ch1.grid(row=9, column=10, sticky=W)
    root2.mainloop()


def sterg2():
    root2 = Toplevel()
    root2.title("Моделирование поперечно-изгибных колебаний стержня")
    root2.geometry("730x560+310+20")

    # root2.resizable(False, False)

    def clean():  # обработчик кнопки очистка
        e_e.delete(0, END)
        d_max_e.delete(0, END)
        d_min_e.delete(0, END)
        P_e.delete(0, END)
        # n_e.delete(0, END)
        w_e.delete(0, END)
        p_e.delete(0, END)
        # s_e.delete(0, END)
        l_e.delete(0, END)
        time_e.delete(0, END)
        #####
        c0_e.delete(0, END)
        a_e.delete(0, END)
        cz_e.delete(0, END)
        #####
        r_var.set(0)
        q1.delete("txt")

    def tableSterg2():
        e, p_nagruzka, w, p, d_max, d_min, len_sterg, time, c0, cz = bspi.get_values(e_e, P_e, w_e, p_e,
                                                                                     d_max_e, d_min_e, l_e,
                                                                                     time_e, c0_e, cz_e)
        # print(e, p_nagruzka, upr_koef, w, p, d_max, d_min, len_sterg, time, c0, cz, sep="\n")

        radiobutton_value = r_var.get()
        error_cheek = 0
        j = bspi.compute_j(d_max, d_min)
        s = bspi.compute_s(d_max, d_min)
        ##заполнение таблицы
        bspi.table_writer(q1, bspi.compute_table(radiobutton_value, len_sterg, e, j))
        # w,_=bspi.compute_table2(radiobutton_value, len_sterg, e, bspi.compute_j(d_max, d_min),
        #       bspi.compute_s(d_max, d_min), p)
        ######################
        # region условия радиокнопки определяющие тип граничных условий
        try:

            #####
            l = bspi.natural_frequency(radiobutton_value, len_sterg, e, j, s, p)
            l.reverse()

            lx = []
            ly = []
            #####
            for w in l:
                if radiobutton_value == 0:
                    x, y = bspi.u_list_0(p, s, w, e, j, len_sterg)
                elif radiobutton_value == 1:
                    x, y = bspi.u_list_1(p, s, w, e, j, len_sterg)
                elif radiobutton_value == 2:
                    x, y = bspi.u_list_2(p, s, w, e, j, c0, len_sterg)
                elif radiobutton_value == 3:
                    x, y = bspi.u_list_3(p, s, w, e, j, c0, len_sterg)
                elif radiobutton_value == 4:
                    x, y = bspi.u_list_4(p, s, w, e, j, c0, cz, len_sterg)
                if None in (x, y):
                    raise ZeroDivisionError
                lx.append((x))
                ly.append((y))


        except ValueError:
            mbox.showerror("Ошибка", "Отрицательное число под корнем")
            error_cheek += 1
        except ZeroDivisionError:
            mbox.showerror("Ошибка", "Происходит деление на ноль")
            error_cheek += 1
        # except:
        #     mbox.showerror("Ошибка", "Неизвстная ошибка при вычислении")
        #     error_cheek += 1
        # endregion

        if error_cheek == 0:  # отрисовка графика
            # bspi.paint_grath(r_var1.get(), lx[i], ly[i], l[i], p, time, radiobutton_value)
            bspi.paint_grath2(lx, ly, l, radiobutton_value)
            lx.clear()
            ly.clear()
            l.clear()

    ###отрисовка интерфеса данного окна
    q1 = Canvas(root2, width=430, height=400, bg="white")
    q1.grid(row=0, column=0, rowspan=8, columnspan=10)
    q1.create_rectangle(2, 2, 431, 401)
    q1.create_rectangle(10, 30, 420.58, 391)
    q1.create_text(239, 15, text="Зависимость собственных частот от массы тела")
    q1.create_text(40, 45, text="m,w", font="Arial 15")
    x = 78.42
    for i in range(6):
        q1.create_line(x, 30, x, 391)
        x += 68.42
    x = 62.81
    for i in range(10):
        q1.create_line(10, x, 420.58, x)
        x += 32.81
    x = 110
    for i in range(5):
        a = str(i + 1)
        q1.create_text(x, 45, text=a, font="Arial 15")
        x += 70
    x = 80
    for i in range(10):
        a = str(i + 1)
        q1.create_text(40, x, text=a, font="Arial 15")
        x += 33

    # Label
    l1 = Label(root2, text="Входные данные:", font="Arial 15")
    l1.grid(row=8, column=0, columnspan=8, sticky=W)
    l2 = Label(root2, text="Граничные условия:", font="Arial 15")
    l2.grid(row=0, column=10, columnspan=3, sticky=W)

    #####
    l3 = Label(root2, text="Дополнительные данные:", font="Arial 15")
    l3.grid(row=5, column=10, columnspan=3, sticky=SW)
    #####

    E_l = Label(root2, text="E=")

    d_max_l = Label(root2, text="D=")
    d_min_l = Label(root2, text="d=")

    P_l = Label(root2, text="P=")
    # n_l = Label(root2, text="n=")
    w_l = Label(root2, text="w=")
    t_l = Label(root2, text="точность=")
    p_l = Label(root2, text="p=")
    # s_l = Label(root2, text="s=")
    l_l = Label(root2, text="l=")
    time_l = Label(root2, text="время=")

    ##########
    c0_l = Label(root2, text="C0=")
    cz_l = Label(root2, text="CZ=")
    a_l = Label(root2, text="Ширина стержня=")
    ##########

    E_l.grid(row=9, column=0, sticky=W)

    d_max_l.grid(row=10, column=0, sticky=W)
    d_min_l.grid(row=11, column=0, sticky=W)

    P_l.grid(row=12, column=0, sticky=W)
    # n_l.grid(row=13, column=0, sticky=W)
    w_l.grid(row=10, column=4, sticky=W)

    p_l.grid(row=9, column=4, sticky=W)
    # s_l.grid(row=10, column=4, sticky=W)
    l_l.grid(row=11, column=4, sticky=W)
    time_l.grid(row=12, column=4, sticky=W)

    c0_l.grid(row=6, column=10, sticky=NW)
    cz_l.grid(row=7, column=10, sticky=NW)
    # a_l.grid(row=7, column=10, sticky=NW)

    # Entry

    e_e = Entry(root2)

    d_max_e = Entry(root2)
    d_min_e = Entry(root2)

    P_e = Entry(root2)
    # n_e = Entry(root2)
    w_e = Entry(root2)

    p_e = Entry(root2)
    # s_e = Entry(root2)
    l_e = Entry(root2)
    time_e = Entry(root2)

    #####
    c0_e = Entry(root2, width=15)
    cz_e = Entry(root2, width=15)
    a_e = Entry(root2, width=15)
    #####

    ######
    e_e.insert(0, 0.89)
    d_max_e.insert(0, 0.12)
    d_min_e.insert(0, 0.1)
    P_e.insert(0, 12)
    # n_e.insert(0, 2)

    p_e.insert(0, 7800)
    # s_e.insert(0, 4)
    w_e.insert(0, 1)
    time_e.insert(0, 0)
    # d_max_e.insert(0, 5)
    c0_e.insert(0, 0.2 * 10 ** 3)
    cz_e.insert(0, 1 * 10 ** 6)
    l_e.insert(0, 1)
    ######

    e_e.grid(row=9, column=1, columnspan=2)

    d_max_e.grid(row=10, column=1, columnspan=2)
    d_min_e.grid(row=11, column=1, columnspan=2)

    P_e.grid(row=12, column=1, columnspan=2)
    # n_e.grid(row=13, column=1, columnspan=2)
    w_e.grid(row=10, column=5, columnspan=2)

    p_e.grid(row=9, column=5, columnspan=2)
    # s_e.grid(row=10, column=5, columnspan=2)
    l_e.grid(row=11, column=5, columnspan=2)
    time_e.grid(row=12, column=5, columnspan=2)

    c0_e.grid(row=6, column=11, sticky=NW)
    cz_e.grid(row=7, column=11, sticky=NW)
    # a_e.grid(row=7, column=11, sticky=NW)

    # frame

    button_frame = Frame(root2)
    button_frame.grid(row=11, column=10, columnspan=6, rowspan=3)
    button_frame_2 = Frame(button_frame)

    # Button
    b1 = Button(button_frame, text="Рассчитать", bg="orange", width=14, command=tableSterg2)
    # b1.grid(row=13, column=11)

    b2 = Button(button_frame, text="Очистить", width=14, command=clean)
    # b2.grid(row=13, column=10)

    b3 = Button(button_frame, text="Расчитать собственные частоты", width=30,
                command=lambda: bspi.table_writer(q1, bspi.compute_table(int(r_var.get()), float(l_e.get()),
                                                                         float(e_e.get()), float(d_max_e.get()))))
    b3.pack(side=TOP)
    button_frame_2.pack(side=TOP)
    b2.pack(side=LEFT)
    b1.pack(side=RIGHT)

    # Radiobutton
    r_var = IntVar()
    r_var.set(0)
    r_1 = Radiobutton(root2, text="Защемлённый стержень", variable=r_var, value=0)
    r_2 = Radiobutton(root2, text="Шарнирно-опёртый стержень", variable=r_var, value=1)
    r_3 = Radiobutton(root2,
                      text="Шарнирно-опёртый стержень на \nупругой опоре (абсолютно жёсткие опоры)\n(требуются дополнительные данные)",
                      variable=r_var, value=2)
    r_4 = Radiobutton(root2,
                      text="Шарнирно-опёртый стержень на \nупругой опоре (абсолютно податливые опоры)\n(требуются дополнительные данные)",
                      variable=r_var, value=3)
    r_5 = Radiobutton(root2,
                      text="Шарнирно-опёртый стержень на \nупругом основании\n(требуются дополнительные данные)",
                      variable=r_var, value=4)
    r_1.grid(row=1, column=10, columnspan=3, sticky=W)
    r_2.grid(row=2, column=10, columnspan=3, sticky=W)
    # r_3.grid(row=3, column=10, columnspan=3, sticky=W)
    # r_4.grid(row=4, column=10, columnspan=3, sticky=W)
    r_5.grid(row=3, column=10, columnspan=3, sticky=W)
    # checkbutton
    r_var1 = IntVar()
    r_var1.set(0)
    ch1 = Checkbutton(root2, text="Анимация", variable=r_var1, onvalue=1, offvalue=0)
    # ch1.grid(row=9, column=10, sticky=W)
    root2.mainloop()


l1 = Label(root, text="ВЫБЕРЕТЕ ВИД ВЫЧИСЛЕНИЙ:")
l1.pack(side=TOP)

button_Balka = Button(root, text="Продольные колебания балки", width=35, command=balka)
button_Balka.pack(side=TOP)
button_Sterg_prodol = Button(root, text="Продольные колебания стержня", width=35, command=sterg)
button_Sterg_prodol.pack(side=TOP)
button_Sterg_poperek = Button(root, text="Поперечно-изгибные колебания стрежня", width=35, command=sterg2)
button_Sterg_poperek.pack(side=TOP)
l = []
lx = []
ly = []
mi = 0

root.mainloop()
