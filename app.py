from tkinter import *
from tkinter import ttk
from settings import ParametrSettings
from model import Model
from analysis import Analysis
from processing import Processing
from config import Config


class App(Tk):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.analysis = Analysis()
        self.parametrs = Config()
        self.processing = Processing()
        self.parametrs.DownloadSettings()
        self.title("МОЭД")
        self.centerWindow()
        self.initUI()

    def centerWindow(self):
        w = 440
        h = 400

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

        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=BOTH)       
        
        frame1 = ttk.Frame(notebook)
        frame2 = ttk.Frame(notebook)
        frame3 = ttk.Frame(notebook)
        frame4 = ttk.Frame(notebook)
        frame5 = ttk.Frame(notebook)
        frame6 = ttk.Frame(notebook)
        frame7 = ttk.Frame(notebook)
        frame8 = ttk.Frame(notebook)
        
        frame1.pack(fill=BOTH, expand=True)
        frame2.pack(fill=BOTH, expand=True)
        frame3.pack(fill=BOTH, expand=True)
        frame4.pack(fill=BOTH, expand=True)
        frame5.pack(fill=BOTH, expand=True)
        frame6.pack(fill=BOTH, expand=True)
        frame7.pack(fill=BOTH, expand=True)
        frame8.pack(fill=BOTH, expand=True)
        
        notebook.add(frame1, text="Лаб. 1")
        notebook.add(frame2, text="Лаб. 2")
        notebook.add(frame3, text="Лаб. 3")
        notebook.add(frame4, text="Лаб. 4")
        notebook.add(frame5, text="Лаб. 5")
        notebook.add(frame6, text="Лаб. 6")
        notebook.add(frame7, text="Лаб. 7")
        notebook.add(frame8, text="Лаб. 8")
        
        self.lab1UI(frame1)
        self.lab2UI(frame2)
        self.lab3UI(frame3)
        self.lab4UI(frame4)
        self.lab5UI(frame5)
        self.lab6UI(frame6)
        self.lab7UI(frame7)
        self.lab8UI(frame8)
        
    
    def lab1UI(self, parent):
        Label(parent,
              text="ТРЕНДЫ"
              ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)

        typeGraph = ["Восходящий", "Низходящий", "Восходящий и низходящий"]

        self.choseGraph1 = StringVar(value=0)

        column = 0
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseGraph1)
            radiobtn_graph.grid(row=1, column=column, padx=5)
            column += 1
        
        del column
        del typeGraph

        Button(
            parent,
            text="Построить линейный тренд",
            command=lambda: self.model.drawLinerTrend(
                a=float(self.parametrs.GetParametr("Parametrs", "a")),
                b=float(self.parametrs.GetParametr("Parametrs", "b")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseGraph1.get())
            )
        ).grid(row=2, column=0, columnspan=3, padx=10,  pady=5)

        Button(
            parent,
            text="Построить экспонентный тренд",
            command=lambda: self.model.drawExponentaTrend(
                alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseGraph1.get())
            )
        ).grid(row=3, column=0, columnspan=3, padx=10)

        Button(
            parent,
            text="Вывести график всех трендов",
            command=lambda: self.model.drawTrend(
                a=float(self.parametrs.GetParametr("Parametrs", "a")),
                b=float(self.parametrs.GetParametr("Parametrs", "b")),
                alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=4, column=0, columnspan=3, padx=10,  pady=5)
    
    def lab2UI(self, parent):
        Label(parent,
              text="ШУМЫ"
              ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)

        Button(
            parent,
            text="Построить график шума на основе линейного конгруэнтного ПСЧ",
            command=lambda: self.model.drawMyRandomNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=1, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            parent,
            text="Построить график шума основанного на встроенном ПСЧ",
            command=lambda: self.model.drawRandomNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=2, column=0, columnspan=3, padx=10)

        Button(
            parent,
            text="Построить график всех шумов",
            command=lambda: self.model.drawNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=3, column=0, columnspan=3, padx=10,  pady=5)     
    
    def lab3UI(self, parent):
        Label(parent,
              text="СТАТИСТИКА"
              ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)
        
        
        typeGraph = ['Шум на основе встроенного генератора', 'Шум на основе написанного генератора']

        self.choseNoise = StringVar(value=0)

        row = 1
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseNoise)
            radiobtn_graph.grid(row=row, column=0, columnspan=3, padx=5)
            row += 1
       
        del row
        del typeGraph
        
        Button(
            parent,
            text='Расчитать статистику',
            command=self.printStatistic
        ).grid(row=3, column=0, columnspan=3, padx=10,  pady=5)

        result = f'Количество значенией:\n'
        result += f'Минимальное значение:\n'
        result += f'Максимальное значение:\n'
        result += f'Среднее значение:\n'
        result += f'Дисперсия:\n'
        result += f'Стандартное отклонение:\n'
        result += f'Ассиметрия:\n'
        result += f'Коэффицент ассиметрии:\n'
        result += f'Эксцесс:\n'
        result += f'Куртозис:\n'
        result += f'Средний квадрат:\n'
        result += f'Ср. квад. ошибка:\n\n'
        
        self.label_statistic = Label(parent, text=result)
        self.label_statistic.grid(row=13, column=0, columnspan=3, padx=10,  pady=5)
    
    def lab4UI(self, parent):
        Label(parent,
              text="СМЕЩЕНИЕ И ИМПУЛЬСЫ"
              ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)
        
        typeGraph = ['Линейный восходящий', 'Линейный низходящий', 'Экспонента восходящая', 'Экспонента низходящая']
        self.choseGraph2 = StringVar(value=0)

        row = 1
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseGraph2)
            radiobtn_graph.grid(row=row, column=0, columnspan=3, padx=5)
            row += 1
       
        del row
        del typeGraph
    
        Button(
            parent,
            text='Построить смещение на графике',
            command=self.drawShift
        ).grid(row=5, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            parent,
            text="Построить импульсы",
            command=lambda: self.model.drawImpulseNoise(
                R=int(self.parametrs.GetParametr("Parametrs", "R2")),
                Rs=int(self.parametrs.GetParametr("Parametrs", "R1"))
            )
        ).grid(row=6, column=0, columnspan=3, padx=10,  pady=5)
    
    def lab5UI(self, parent):
        Label(parent,
              text="ГАРМОНИКИ"
              ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)
    
        Button(
            parent,
            text='Вывести гармонический процесс',
            command=lambda: self.model.drawHarm(
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
            )
        ).grid(row=1, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            parent,
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
        ).grid(row=2, column=0, columnspan=3, padx=10,  pady=5)

        Button(
            parent,
            text='Вывести гармонический процесс с повышением f0 с указанным шагом',
            command=lambda: self.model.drawHarms(
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                step=float(self.parametrs.GetParametr("Parametrs", "step"))
            )
        ).grid(row=3, column=0, columnspan=3, padx=10,  pady=5)
    
    def lab6UI(self, parent):
        Label(parent,
              text="ГИСТАГРАМА"
        ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)
    
        typeGraph = ['Линейный тренд', 'Экспонентный тренд', 'Шум', 'Гармоника']

        self.choseHis = StringVar(value=0)

        row = 1
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseHis)
            radiobtn_graph.grid(row=row, column=0, columnspan=3, padx=5)
            row += 1
       
        del row
        del typeGraph
        
        Button(
            parent,
            text="Построить гистаграмму",
            command=self.drawHistogram
        ).grid(row=5, column=0, columnspan=3, padx=10,  pady=5)
    
    def lab7UI(self, parent):
        Label(
            parent,
            text="АВТОКОРЯЛЛЯЦИЯ И ВЗАИМНОКОРРЕЛЯЦИОННАЯ ФУНКЦИИ"
        ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)
        
        typeGraph = ['Шум встроенный', 'Шум написанный', 'Гармоника', 'Линейный тренд', 'Экспонентный тренд']

        self.choseAuto = StringVar(value=0)

        row = 1
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseAuto)
            radiobtn_graph.grid(row=row, column=0, columnspan=3, padx=5)
            row += 1
       
        del row
        del typeGraph

        Button(
            parent,
            text="Построить график автокорялляции",
            command=self.drawAutoKor
        ).grid(row=7, column=0, columnspan=3, padx=10,  pady=5)

        Button(
            parent,
            text="Построить взаимокорреляционную функцию",
            command=self.drawTwoAutoKor
        ).grid(row=8, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            parent,
            text="Удалить смещение в данных",
            command=self.antiShift
        ).grid(row=9, column=0, columnspan=3, padx=10,  pady=5)
        
        typeGraph = ['Шум встроенный c импульсами', 'Гармоника c импульсами']
        
        self.choseImpulse = StringVar(value=0)

        row = 10
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseImpulse)
            radiobtn_graph.grid(row=row, column=0, columnspan=3, padx=5)
            row += 1
       
        del row
        del typeGraph
        
        Button(
            parent,
            text="Удалить неправдоподобных значений в данных",
            command=self.antiSpike
        ).grid(row=12, column=0, columnspan=3, padx=10,  pady=5)
        
    def lab8UI(self, parent):
        Label(parent,
              text="СЛОЖЕНИЕ ДАННЫХ"
              ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)

        typeGraph = ["Линейный тренд + гармоника", "Экспонентный тренд + шум"]

        self.choseSum = StringVar(value=0)

        column = 0
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseSum)
            radiobtn_graph.grid(row=1, column=column, padx=5)
            column += 1
        
        del column
        del typeGraph
        
        Button(
            parent,
            text="Сложить данные",
            command=self.addModel
        ).grid(row=2, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            parent,
            text="Удаление линейного тренда"
        ).grid(row=3, column=0, columnspan=3, padx=10,  pady=5)
        
        Button(
            parent,
            text="Удаление нелинейного тренда"
        ).grid(row=4, column=0, columnspan=3, padx=10,  pady=5)            
        
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
    
    def drawHistogram(self):
        if int(self.choseHis.get()) == 0:
            self.analysis.histograma(
                self.model.getLinerTrend(
                    a=float(self.parametrs.GetParametr("Parametrs", "a")),
                    b=float(self.parametrs.GetParametr("Parametrs", "b")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=0
                ),
                M= int(self.parametrs.GetParametr("Parametrs", "M"))
            )
        elif int(self.choseHis.get()) == 1:
            self.analysis.histograma(
                self.model.getExponentaTrend(
                    alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                    beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=0
                ),
                M= int(self.parametrs.GetParametr("Parametrs", "M"))
            )
        elif int(self.choseHis.get()) == 2:
            self.analysis.histograma(
                self.model.getNoise(
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=0
                ),
                M= int(self.parametrs.GetParametr("Parametrs", "M"))
            )
        elif int(self.choseHis.get()) == 3:
            self.analysis.histograma(
                self.model.getHarm(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                    f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                    dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                    thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
                ),
                M= int(self.parametrs.GetParametr("Parametrs", "M"))
            )
    
    def drawAutoKor(self):
        if int(self.choseAuto.get()) == 0:
            self.analysis.acf(
                self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=0
                )
            )
        elif int(self.choseAuto.get()) == 1:
            self.analysis.acf(
                self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=1
                )
            )
        elif int(self.choseAuto.get()) == 2:
            self.analysis.acf(
                self.model.getHarm(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                    f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                    dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                    thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
                )
            )
        elif int(self.choseAuto.get()) == 3:
            self.analysis.acf(
                self.model.getLinerTrend(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    a=float(self.parametrs.GetParametr("Parametrs", "a")),
                    b=float(self.parametrs.GetParametr("Parametrs", "b")),
                    type=0
                )
            )
        elif int(self.choseAuto.get()) == 4:
            self.analysis.acf(
                self.model.getExponentaTrend(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                    beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                    type=1
                )
            )
    
    def drawTwoAutoKor(self):
        if int(self.choseAuto.get()) == 0:
            self.analysis.ccf(
                self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=0
                ),
                self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=0
                ),
            )
        elif int(self.choseAuto.get()) == 1:
            self.analysis.ccf(
                self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=1
                ),
                self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=1
                )
            )
        elif int(self.choseAuto.get()) == 2:
            self.analysis.ccf(
                self.model.getHarm(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                    f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                    dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                    thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
                ),
                self.model.getHarm(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    A0=float(self.parametrs.GetParametr("Parametrs", "A1")),
                    f0=float(self.parametrs.GetParametr("Parametrs", "f1")),
                    dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                    thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
                )
            )
    
    def antiShift(self):
        if int(self.choseAuto.get()) == 0:
            self.processing.antiShift(
                self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=0
                )
            )
        elif int(self.choseAuto.get()) == 1:
            self.processing.antiShift(
                self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=1
                )
            )
        elif int(self.choseAuto.get()) == 2:
            self.processing.antiShift(
                self.model.getHarm(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                    f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                    dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                    thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
                )
            )
        elif int(self.choseAuto.get()) == 3:
            self.processing.antiShift(
                self.model.getLinerTrend(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    a=float(self.parametrs.GetParametr("Parametrs", "a")),
                    b=float(self.parametrs.GetParametr("Parametrs", "b")),
                    type=0
                )
            )
        elif int(self.choseAuto.get()) == 4:
            self.processing.antiShift(
                self.model.getExponentaTrend(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                    beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                    type=1
                )
            ) 
    
    def antiSpike(self):
        if int(self.choseImpulse.get()) == 0:
            self.processing.antiSpike(
                data=self.model.getImpulseNoise(
                    data=self.model.getNoise(
                        Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                        N=int(self.parametrs.GetParametr("Parametrs", "N")),
                        type=0
                    )
                )
            )
        elif int(self.choseImpulse.get()) == 1:
            self.processing.antiSpike(
                data=self.model.getImpulseNoise(
                    data=self.model.getHarm(
                        N=int(self.parametrs.GetParametr("Parametrs", "N")),
                        A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                        f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                        dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                        thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
                    )
                )
            )
    
    def addModel(self):
        if int(self.choseSum.get()) == 0:
            self.model.addModel(
                data1=self.model.getLinerTrend(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    a=float(self.parametrs.GetParametr("Parametrs", "a")),
                    b=float(self.parametrs.GetParametr("Parametrs", "b")),
                    type=0
                ),
                data2=self.model.getHarm(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
                    f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
                    dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
                    thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
                )
            )
        elif int(self.choseSum.get()) == 1:
            self.model.addModel(
                data1=self.model.getExponentaTrend(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                    beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                    type=0
                ),
                data2=self.model.getNoise(
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    type=0
                )
            )