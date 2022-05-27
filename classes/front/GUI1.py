import tkinter as tk


class Win_standart():
    def __init__(self, name: str, geometry: tuple, resizeble: tuple = (False, False)):
        self.root = tk.Tk()
        self.root.title(name)
        self.root.geometry(f"{geometry[0]}x{geometry[1]}+{geometry[2]}+{geometry[3]}")
        self.root.resizable(resizeble[0], resizeble[1])

    def start(self):
        self.root.mainloop()

    def create_radiobutton_menu(self):
        menu = tk.Menu()
        self.root.config(menu=menu)


if __name__ == '__main__':
    w = Win_standart("окно1", (300, 300, 100, 100))
    w.start()
