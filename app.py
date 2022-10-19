from tkinter import *
from tkinter import ttk
from settings import ParametrSettings
from model import Model
from analysis import Analysis
from config import Config


class App(Tk):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.analysis = Analysis()
        self.parametrs = Config()
        self.parametrs.DownloadSettings()
        self.title("МОЭД")
        self.centerWindow()
        self.initUI()

    def centerWindow(self):
        w = 450
        h = 800

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def openParametrSettings(self):
        ParametrSettings(self)

    def initUI(self):
        mainmenu = Menu()
        self.config(menu=mainmenu)

        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Выход", command=self.destroy)
        mainmenu.add_cascade(label="Файл", menu=filemenu)

        settings = Menu(mainmenu, tearoff=0)
        settings.add_command(label="Настройки параметров", command=self.openParametrSettings)
        mainmenu.add_cascade(label="Настройки", menu=settings)

        canvas=Canvas(self)
        canvas.pack(side=LEFT,fill=BOTH,expand=1)
        scrollbar=Scrollbar(self,orient=VERTICAL,command=canvas.yview)
        scrollbar.pack(side=RIGHT,fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        mainFrame=Frame(canvas)
        canvas.create_window((0,0),window=mainFrame,anchor="nw")
        
        
        
        Label(mainFrame,
              text="ТРЕНДЫ"
              ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)

        typeGraph = ["Восходящий", "Низходящий", "Восходящий и низходящий"]

        self.choseGraph1 = StringVar(value=0)

        column = 0
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(mainFrame, text=typeGraph[index], value=index, variable=self.choseGraph1)
            radiobtn_graph.grid(row=1, column=column, padx=5)
            column += 1
        
        del column
        del typeGraph

        Button(
            mainFrame,
            text="Построить линейный тренд",
            command=lambda: self.model.drawLinerTrend(
                a=float(self.parametrs.GetParametr("Parametrs", "a")),
                b=float(self.parametrs.GetParametr("Parametrs", "b")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseGraph1.get())
            )
        ).grid(row=2, column=0, columnspan=3, padx=10,  pady=5)

        Button(
            mainFrame,
            text="Построить экспонентный тренд",
            command=lambda: self.model.drawExponentaTrend(
                alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseGraph1.get())
            )
        ).grid(row=3, column=0, columnspan=3, padx=10)

        Button(
            mainFrame,
            text="Вывести график всех трендов",
            command=lambda: self.model.drawTrend(
                a=float(self.parametrs.GetParametr("Parametrs", "a")),
                b=float(self.parametrs.GetParametr("Parametrs", "b")),
                alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=4, column=0, columnspan=3, padx=10,  pady=5)
        
        Label(mainFrame,
              text="ШУМЫ"
              ).grid(row=5, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)

        Button(
            mainFrame,
            text="Построить график шума на основе линейного конгруэнтного ПСЧ",
            command=lambda: self.model.drawMyRandomNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=6, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            mainFrame,
            text="Построить график шума основанного на встроенном ПСЧ",
            command=lambda: self.model.drawRandomNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=7, column=0, columnspan=3, padx=10)

        Button(
            mainFrame,
            text="Построить график всех шумов",
            command=lambda: self.model.drawNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=8, column=0, columnspan=3, padx=10,  pady=5)
    
        Label(mainFrame,
              text="СТАТИСТИКА"
              ).grid(row=9, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)
        
        
        typeGraph = ['Шум на основе встроенного генератора', 'Шум на основе написанного генератора']

        self.choseNoise = StringVar(value=0)

        row = 10
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(mainFrame, text=typeGraph[index], value=index, variable=self.choseNoise)
            radiobtn_graph.grid(row=row, column=0, columnspan=3, padx=5)
            row += 1
       
        del row
        del typeGraph
        
        Button(
            mainFrame,
            text='Расчитать статистику',
            command=self.printStatistic
        ).grid(row=12, column=0, columnspan=3, padx=10,  pady=5)

        result = f'Количество значенией:\n'
        result += f'Минимальное значение:\n'
        result += f'Максимальное значение:\n'
        result += f'Среднее значение:\n'
        result += f'Дисперсия:\n'
        result += f'Стандартное отклонение:\n'
        result += f'Ассиметрия:\tКоэффицент ассиметрии:\n'
        result += f'Эксцесс:\tкуртозис:\n'
        result += f'Средний квадрат:\n'
        result += f'Среднеквадратическая ошибка:\n\n'
        
        self.label_statistic = Label(mainFrame, text=result)
        self.label_statistic.grid(row=13, column=0, columnspan=3, padx=10,  pady=5)
        
        
        Label(mainFrame,
              text="СМЕЩЕНИЕ И ИМПУЛЬСЫ"
              ).grid(row=14, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)
        
        typeGraph = ['Линейный восходящий', 'Линейный низходящий', 'Экспонента восходящая', 'Экспонента низходящая']
        self.choseGraph2 = StringVar(value=0)

        row = 15
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(mainFrame, text=typeGraph[index], value=index, variable=self.choseGraph2)
            radiobtn_graph.grid(row=row, column=0, columnspan=3, padx=5)
            row += 1
       
        del row
        del typeGraph
    
        Button(
            mainFrame,
            text='Построить смещение на графике',
            command=self.drawShift
        ).grid(row=19, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            mainFrame,
            text="Построить импульсы",
            command=lambda: self.model.drawImpulseNoise(
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                R=int(self.parametrs.GetParametr("Parametrs", "R2")),
                Rs=int(self.parametrs.GetParametr("Parametrs", "R1"))
            )
        ).grid(row=20, column=0, columnspan=3, padx=10,  pady=5)
    
        Label(mainFrame,
              text="ГАРМОНИКИ"
              ).grid(row=21, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)
    
        Button(
            mainFrame,
            text='Вывести гармонический процесс',
            command=lambda: self.model.drawHarm(
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
            )
        ).grid(row=22, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            mainFrame,
            text='Вывести гармонический процесс с суммой трех гармоник',
            command=lambda: self.model.draw3In1Harm(
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                A1=float(self.parametrs.GetParametr("Parametrs", "A1")),
                A2=float(self.parametrs.GetParametr("Parametrs", "A2")),
                f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                f1=float(self.parametrs.GetParametr("Parametrs", "f1")),
                f2=float(self.parametrs.GetParametr("Parametrs", "f2")),
                dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
            )
        ).grid(row=23, column=0, columnspan=3, padx=10,  pady=5)

        Button(
            mainFrame,
            text='Вывести гармонический процесс с повышением f0 с указанным шагом',
            command=lambda: self.model.drawHarms(
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                step=float(self.parametrs.GetParametr("Parametrs", "step"))
            )
        ).grid(row=24, column=0, columnspan=3, padx=10,  pady=5)
        
     
    def printStatistic(self):
        result = self.analysis.statistics(
            self.model.getNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseNoise.get())
            )
        )
        result += '\n\n'
        result += self.analysis.stationarity(
            self.model.getNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseNoise.get())
            )
        )
        
        self.label_statistic.configure(text=result)

    
    def drawShift(self):
        if int(self.choseGraph2.get()) == 0:
            self.model.drawShiftData(
                data=self.model.getLinerTrend(
                    a=float(self.parametrs.GetParametr("Parametrs", "a")),
                    b=float(self.parametrs.GetParametr("Parametrs", "b")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=0
                    ),
                shift=float(self.parametrs.GetParametr("Parametrs", "Shift")),
                N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom")),
                N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
            )
        elif int(self.choseGraph2.get()) == 1:
            self.model.drawShiftData(
                data=self.model.getLinerTrend(
                    a=float(self.parametrs.GetParametr("Parametrs", "a")),
                    b=float(self.parametrs.GetParametr("Parametrs", "b")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=1
                    ),
                shift=float(self.parametrs.GetParametr("Parametrs", "Shift")),
                N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom")),
                N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
            )
        elif int(self.choseGraph2.get()) == 2:
            self.model.drawShiftData(
                data=self.model.getExponentaTrend(
                    alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                    beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=0
                    ),
                shift=float(self.parametrs.GetParametr("Parametrs", "Shift")),
                N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom")),
                N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
            )
        elif int(self.choseGraph2.get()) == 3:
            self.model.drawShiftData(
                data=self.model.getExponentaTrend(
                    alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                    beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=1
                    ),
                shift=float(self.parametrs.GetParametr("Parametrs", "Shift")),
                N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom")),
                N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
            )