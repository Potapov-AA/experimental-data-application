from tkinter import *
from config import Config


class ParametrSettings(Toplevel):
    def __init__(self, parent):
        self.parametrs = Config()
        super().__init__(parent)
        self.title("Настройки параметров")
        self.centerWindow()

        Label(self, text="Общие параметры").grid(
            column=0, row=0, columnspan=3, sticky=E+W, padx=5, pady=5)
        
        Label(self, text="N =").grid(column=0, row=1, padx=10, sticky=W)
        self.entry_N = Entry(self, width=10, justify=CENTER)
        self.entry_N.grid(column=1, row=1, padx=5, sticky=E)
        self.entry_N.insert(0, self.parametrs.GetParametr("Parametrs", "N"))
        Button(self, text="Сохранить", width=10,
               command=lambda: self.save("N", self.entry_N.get())).grid(column=2, row=1, padx=5)

        Label(self, text="Линейный тренд (y=ax+b)").grid(column=0,
                                                         row=2, columnspan=3, sticky=E+W, padx=5, pady=5)

        Label(self, text="a =").grid(column=0, row=3, padx=10, sticky=W)
        self.entry_a = Entry(self, width=10, justify=CENTER)
        self.entry_a.grid(column=1, row=3, padx=5, sticky=E)
        self.entry_a.insert(0, self.parametrs.GetParametr("Parametrs", "a"))
        Button(self, text="Сохранить", width=10,
               command=lambda: self.save("a", self.entry_a.get())).grid(column=2, row=3, padx=5)

        Label(self, text="b =").grid(column=0, row=4, padx=10, sticky=W)
        self.entry_b = Entry(self, width=10, justify=CENTER)
        self.entry_b.grid(column=1, row=4, padx=5, sticky=E)
        self.entry_b.insert(0, self.parametrs.GetParametr("Parametrs", "b"))
        Button(self, text="Сохранить", width=10,
               command=lambda: self.save("b", self.entry_b.get())).grid(column=2, row=4, padx=5)

        Label(self, text="Экспонентный тренд (y=beta*e^alpha*x)").grid(column=0,
                                                         row=5, columnspan=3, sticky=E+W, padx=5, pady=5)
        
        Label(self, text="alpha =").grid(column=0, row=6, padx=10, sticky=W)
        self.entry_alpha = Entry(self, width=10, justify=CENTER)
        self.entry_alpha.grid(column=1, row=6, padx=5, sticky=E)
        self.entry_alpha.insert(0, self.parametrs.GetParametr("Parametrs", "alpha"))
        Button(self, text="Сохранить", width=10,
               command=lambda: self.save("alpha", self.entry_alpha.get())).grid(column=2, row=6, padx=5)
        
        Label(self, text="beta =").grid(column=0, row=7, padx=10, sticky=W)
        self.entry_beta = Entry(self, width=10, justify=CENTER)
        self.entry_beta.grid(column=1, row=7, padx=5, sticky=E)
        self.entry_beta.insert(0, self.parametrs.GetParametr("Parametrs", "beta"))
        Button(self, text="Сохранить", width=10,
               command=lambda: self.save("beta", self.entry_beta.get())).grid(column=2, row=7, padx=5)

    def centerWindow(self):
        w = 235
        h = 400

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    
    def save(self, parameterName, value):
        self.parametrs.UpdateParametr("Parametrs", parameterName, value)
