from tkinter import *
from config import Config


class ParametrSettings(Toplevel):
    def __init__(self, parent):
        self.config = Config()
        super().__init__(parent)
        self.title("Настройки параметров")
        self.centerWindow()

        Label(self, text="Общие параметры").grid(
            column=0, row=0, columnspan=3, sticky=E+W, padx=5, pady=5)
        Label(self, text="N =").grid(column=0, row=1, padx=10, sticky=W)
        self.entry_N = Entry(self, width=10, justify=CENTER)
        self.entry_N.grid(column=1, row=1, padx=5, sticky=E)
        self.entry_N.insert(0, self.config.GetParametr("Parametrs", "N"))
        Button(self, text="Сохранить", width=10,
               command=self.saveN).grid(column=2, row=1, padx=5)

        Label(self, text="Линейный тренд (y=ax+b)").grid(column=0,
                                                         row=2, columnspan=3, sticky=E+W, padx=5, pady=5)

        Label(self, text="a =").grid(column=0, row=3, padx=10, sticky=W)
        self.entry_a = Entry(self, width=10, justify=CENTER)
        self.entry_a.grid(column=1, row=3, padx=5, sticky=E)
        self.entry_a.insert(0, self.config.GetParametr("Parametrs", "a"))
        Button(self, text="Сохранить", width=10,
               command=self.saveA).grid(column=2, row=3, padx=5)

        Label(self, text="b =").grid(column=0, row=4, padx=10, sticky=W)
        self.entry_b = Entry(self, width=10, justify=CENTER)
        self.entry_b.grid(column=1, row=4, padx=5, sticky=E)
        self.entry_b.insert(0, self.config.GetParametr("Parametrs", "b"))
        Button(self, text="Сохранить", width=10,
               command=self.saveB).grid(column=2, row=4, padx=5)

    def centerWindow(self):
        w = 220
        h = 400

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def saveA(self):
        self.config.UpdateParametr("Parametrs", "a", self.entry_a.get())

    def saveB(self):
        self.config.UpdateParametr("Parametrs", "b", self.entry_b.get())

    def saveN(self):
        self.config.UpdateParametr("Parametrs", "N", self.entry_N.get())
