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
#     def __ff(self):
#         print("жопа")
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
a = "dfdf{name} fdkjfdkf{r}{name}"
print(a.format(name="dima", r=12))
