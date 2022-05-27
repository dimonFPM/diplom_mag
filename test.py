# import tkinter as tk
#
#
# class Label_entry():
#     def __init__(self, root_frame, name):
#         self.__f = tk.Frame(root_frame)
#         self.__e = tk.Entry(self.__f)
#         # self.__e.insert(0, "22")
#         self.__l = tk.Label(self.__f, text=name)
#         self.__pack()
#
#     def __pack(self):
#         self.__l.pack(side=tk.LEFT)
#         self.__e.pack(side=tk.LEFT)
#         self.__f.pack(side=tk.TOP)
#
#     def get(self):
#         return self.__e.get()
#
#     def set(self, x):
#         self.__e.delete(0, tk.END)
#         self.__e.insert(0, x)
#
#
# class Label_entry_blok():
#     pass
# def f1():
#     print(chislo.get())
#
#
# root_win = tk.Tk()
# b = tk.Button(root_win, text="кнопка!!!", command=f1)
# b.pack(side=tk.TOP)
# frame = tk.Frame(root_win)
# frame.pack(side=tk.TOP)
#
# chislo = Label_entry(frame, "chislo")
# chislo2 = Label_entry(frame, "chislo2")
# chislo3 = Label_entry(root_win, "chislo3")
#
# print(chislo.get())
# root_win.mainloop()
#
# import threading
#
#
# def f1(name):
#     for i in range(25):
#         print(f"\nя поток {name}, но не главный////{i}")
#
#
#
# name = "поток1"
# th1 = threading.Thread(target=f1, name=name, args=(name,))
# th1.start()
# for i in range(100):
#     print(f"\nя цикл, его {i} итерация")
import matplotlib.pyplot as plt

x = [i for i in range(100)]
y = [i ** 2 for i in x]
y2 = [i ** 3 for i in x]
fig = plt.figure("это")
plt.title("кака")
plt.subplot(121)
plt.plot(x, y)
plt.subplot(122)
plt.plot(x, y2)

plt.show()
