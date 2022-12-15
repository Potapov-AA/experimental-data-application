from tkinter import *
from config import Config
import tkinter.ttk as ttk


class ParametrSettings(Toplevel):
       def __init__(self, parent):
              self.parametrs = Config()
              super().__init__(parent)
              self.title("Настройки параметров")
              self.centerWindow()

              notebook = ttk.Notebook(self)
              notebook.pack(expand=True, fill=BOTH)       
              
              frame1 = ttk.Frame(notebook)
              frame2 = ttk.Frame(notebook)
              frame3 = ttk.Frame(notebook)
              
              frame1.pack(fill=BOTH, expand=True)
              frame2.pack(fill=BOTH, expand=True)
              frame3.pack(fill=BOTH, expand=True)
              
              notebook.add(frame1, text="Стр. 1")
              notebook.add(frame2, text="Стр. 2")
              notebook.add(frame3, text="Стр. 3")
              
              self.page1UI(frame1)
              self.page2UI(frame2)
              self.page3UI(frame3)
       
       def page1UI(self, parent):
              Label(parent, text="Общие параметры").pack(anchor=N, fill=X, pady=[20, 10])
              self.drawParameter("N =", "N", parent)
              
              Label(parent, text="Линейный график").pack(anchor=N, fill=X, pady=[15, 10])
              self.drawParameter("a =", "a", parent)
              self.drawParameter("b =", "b", parent)
              
              Label(parent, text="График экспоненты").pack(anchor=N, fill=X, pady=[15, 10])
              self.drawParameter("alpha =", "alpha", parent)
              self.drawParameter("beta =", "beta", parent)
              
              Label(parent, text="Гармоники (синусойда)").pack(anchor=N, fill=X, pady=[15, 10])
              
              self.drawParameter("A0 =", "A0", parent)
              self.drawParameter("A1 =", "A1", parent)
              self.drawParameter("A2 =", "A2", parent)
              self.drawParameter("f0 =", "f0", parent)
              self.drawParameter("f1 =", "f1", parent)
              self.drawParameter("f2 =", "f2", parent)
              self.drawParameter("dt =", "dt", parent)
              self.drawParameter("step =", "step", parent)
              self.drawParameter("thetta =", "thetta", parent)
              
              
              Label(parent, text="Шумы").pack(anchor=N, fill=X, pady=[15, 10])
              self.drawParameter("R =", "R", parent)
              
              Label(parent, text="Смещение и импульсы").pack(anchor=N, fill=X, pady=[15, 10])
              self.drawParameter("Shift =", "Shift", parent)
              self.drawParameter("From =", "ShiftFrom", parent)
              self.drawParameter("To =", "ShiftTo", parent)
              self.drawParameter("R1 =", "R1", parent)
              self.drawParameter("R2 =", "R2", parent)
              
              
              
       
       def page2UI(self, parent):
              Label(parent, text="Гистограмма").pack(anchor=N, fill=X, pady=[20, 10])
              self.drawParameter("M =", "M", parent)
              
              Label(parent, text="Размеры скользящего \nсреднего").pack(anchor=N, fill=X, pady=[15, 10])
              self.drawParameter("W1 =", "W1", parent)
              self.drawParameter("W2 =", "W2", parent)
              self.drawParameter("W3 =", "W3", parent)
              
              Label(parent, text="Размеры прямоугольных \nокн").pack(anchor=N, fill=X, pady=[15, 10])
              self.drawParameter("L1 =", "L1", parent)
              self.drawParameter("L2 =", "L2", parent)
              self.drawParameter("L3 =", "L3", parent)
              
              Label(parent, text="Метод накопления").pack(anchor=N, fill=X, pady=[15, 10])
              
              self.drawParameter("M step =", "stepM", parent)
              
              Label(parent, text="Импульсная реакция").pack(anchor=N, fill=X, pady=[15, 10])
              
              self.drawParameter("fc =", "fc", parent)
              self.drawParameter("fc1 =", "fc1", parent)
              self.drawParameter("fc2 =", "fc2", parent)
              self.drawParameter("m =", "m for lpf", parent)
              
              Label(parent, text="Ударный слог").pack(anchor=N, fill=X, pady=[15, 10])
                                                                  
              self.drawParameter("c1 = ", "c1", parent)
              self.drawParameter("c1 = ", "c1", parent)
              
              self.drawParameter("n1 = ", "n1", parent)
              self.drawParameter("n2 = ", "n2", parent)
              self.drawParameter("n3 = ", "n3", parent)
              self.drawParameter("n4 = ", "n4", parent)
       
       def page3UI(self, parent):
              Label(parent, text="Фрагмент звукового файла").pack(anchor=N, fill=X, pady=[20, 10])
              self.drawParameter("sN1 =", "sN1", parent)
              self.drawParameter("sN2 =", "sN2", parent)
            
       def centerWindow(self):
              w = 300
              h = 780

              sw = self.winfo_screenwidth()
              sh = self.winfo_screenheight()

              x = (sw - w) / 2
              y = (sh - h) / 2
              self.geometry('%dx%d+%d+%d' % (w, h, x, y))

       def drawParameter(self, text, parametrName, parent):
              frame = ttk.Frame(parent)
              frame.pack(anchor=N, fill=X)
              Label(frame, text=text).pack(anchor=N, side=LEFT, padx=[15, 10], pady=[5,0], fill=X)
              entry = Entry(frame, width=6, justify=CENTER)
              entry.pack(anchor=N, side=LEFT, padx=[10, 0], pady=[5,0], fill=X)
              entry.insert(0, self.parametrs.GetParametr("Parametrs", parametrName))
              Button(frame, 
                     text="Сохранить",
                     command=lambda: self.save(parametrName, entry.get())
              ).pack(anchor=N, side=RIGHT, fill=X, padx=[0, 15])
       
       def save(self, parameterName, value):
              self.parametrs.UpdateParametr("Parametrs", parameterName, value)
        
