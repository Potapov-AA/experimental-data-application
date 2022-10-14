from tkinter import *
from tkinter import ttk

class ParametrSettings(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Настройки параметров")
        self.centerWindow()
        
        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='ws')
        
        notebook  = ttk.Notebook(self, style='lefttab.TNotebook')
        f1 = Frame(notebook, height=400)
        f2 = Frame(notebook, height=400)
        notebook.add(f1, text='Frame 1')
        notebook.add(f2, text='Frame 2')
        notebook.pack(fill=BOTH)
    
    def centerWindow(self):
        w = 300
        h = 400

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    