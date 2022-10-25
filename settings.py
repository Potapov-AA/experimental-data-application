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

              self.drawParameter("N =", 1, "N")

              Label(self, text="Линейный тренд").grid(column=0,
                                                      row=2, 
                                                      columnspan=3, 
                                                      sticky=E+W, 
                                                      padx=5, 
                                                      pady=5)

              self.drawParameter("a =", 3, "a")
              self.drawParameter("b =", 4, "b")

              Label(self, text="Экспонентный тренд").grid(column=0,
                                                          row=5, 
                                                          columnspan=3, 
                                                          sticky=E+W, 
                                                          padx=5, 
                                                          pady=5)

              self.drawParameter("alpha =", 6, "alpha")
              self.drawParameter("beta =", 7, "beta")

              Label(self, text="Шумы").grid(column=0, 
                                            row=8,
                                            columnspan=3, 
                                            sticky=E+W, 
                                            padx=5, 
                                            pady=5)

              self.drawParameter("R =", 9, "R")
              
              Label(self, text="Смещение и импульсы").grid(column=0, 
                                                           row=10, 
                                                           columnspan=3, 
                                                           sticky=E+W, 
                                                           padx=5, 
                                                           pady=5)
              
              self.drawParameter("Shift =", 11, "Shift")
              self.drawParameter("From =", 12, "ShiftFrom")
              self.drawParameter("To =", 13, "ShiftTo")
              self.drawParameter("R1 =", 14, "R1")
              self.drawParameter("R2 =", 15, "R2")
              
              Label(self, text="Гармоники").grid(column=0, 
                                                 row=16, 
                                                 columnspan=3, 
                                                 sticky=E+W, 
                                                 padx=5, 
                                                 pady=5)
              
              self.drawParameter("A0 =", 17, "A0")
              self.drawParameter("A1 =", 18, "A1")
              self.drawParameter("A2 =", 19, "A2")
              self.drawParameter("f0 =", 20, "f0")
              self.drawParameter("f1 =", 21, "f1")
              self.drawParameter("f2 =", 22, "f2")
              self.drawParameter("dt =", 23, "dt")
              self.drawParameter("step =", 24, "step")
              self.drawParameter("thetta =", 25, "thetta")
              
              Label(self, text="Гистограмма").grid(column=0, 
                                                   row=26, 
                                                   columnspan=3, 
                                                   sticky=E+W, 
                                                   padx=5, 
                                                   pady=5)
              
              self.drawParameter("M =", 27, "M")
              
       def centerWindow(self):
              w = 235
              h = 800

              sw = self.winfo_screenwidth()
              sh = self.winfo_screenheight()

              x = (sw - w) / 2
              y = (sh - h) / 2
              self.geometry('%dx%d+%d+%d' % (w, h, x, y))

       def drawParameter(self, text, row, parametrName):
              Label(self, text=text).grid(column=0, row=row, padx=10, sticky=W)
              entry = Entry(self, width=10, justify=CENTER)
              entry.grid(column=1, row=row, padx=5, sticky=E)
              entry.insert(0, self.parametrs.GetParametr("Parametrs", parametrName))
              Button(self, text="Сохранить", width=10,
                     command=lambda: self.save(parametrName, entry.get())).grid(column=2, row=row, padx=5)
       
       def save(self, parameterName, value):
              self.parametrs.UpdateParametr("Parametrs", parameterName, value)
        
