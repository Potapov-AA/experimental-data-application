from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd 
from tkinter import font
import numpy as np
from settings import ParametrSettings
from model import Model
from analysis import Analysis
from processing import Processing
from config import Config
from inout import InOut


class App(Tk):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.analysis = Analysis()
        self.processing = Processing()
        self.parametrs = Config()
        self.inout = InOut()
        
        self.currentData = []
        self.currentSoundData = []
        
        self.font = font.Font(family= "Verdana", size=12, weight="normal", slant="roman")
        
        self.parametrs.DownloadSettings()
        self.title("Обработчик данных")
        self.centerWindow()
        self.initUI()

    def centerWindow(self):
        w = 800
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
        filemenu.add_command(label="Открыть файл с данными", command=self.openBinaryFile)
        filemenu.add_command(label="Сохранить текущий файл с данными", command=self.saveBinaryFile)
        filemenu.add_command(label="Открыть звуковой файл", command=self.openSoundFile)
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
        frame9 = ttk.Frame(notebook)
        frame10 = ttk.Frame(notebook)
        frame11 = ttk.Frame(notebook)
        frame12 = ttk.Frame(notebook)
        frame13 = ttk.Frame(notebook)
        
        frame1.pack(fill=BOTH, expand=True)
        frame2.pack(fill=BOTH, expand=True)
        frame3.pack(fill=BOTH, expand=True)
        frame4.pack(fill=BOTH, expand=True)
        frame5.pack(fill=BOTH, expand=True)
        frame6.pack(fill=BOTH, expand=True)
        frame7.pack(fill=BOTH, expand=True)
        frame8.pack(fill=BOTH, expand=True)
        frame9.pack(fill=BOTH, expand=True)
        frame10.pack(fill=BOTH, expand=True)
        frame11.pack(fill=BOTH, expand=True)
        frame12.pack(fill=BOTH, expand=True)
        frame13.pack(fill=BOTH, expand=True)
        
        notebook.add(frame1, text="Л. 1")
        notebook.add(frame2, text="Л. 2")
        notebook.add(frame3, text="Л. 3")
        notebook.add(frame4, text="Л. 4")
        notebook.add(frame5, text="Л. 5")
        notebook.add(frame6, text="Л. 6")
        notebook.add(frame7, text="Л. 7")
        notebook.add(frame8, text="Л. 8")
        notebook.add(frame9, text="Л. 9")
        notebook.add(frame10, text="Л. 10")
        notebook.add(frame11, text="Л. 11")
        notebook.add(frame12, text="Л. 12")
        notebook.add(frame13, text="Л. 13")
        
        self.lab1UI(frame1)
        # self.lab2UI(frame2)
        # self.lab3UI(frame3)
        # self.lab4UI(frame4)
        # self.lab5UI(frame5)
        # self.lab6UI(frame6)
        # self.lab7UI(frame7)
        # self.lab8UI(frame8)
        # self.lab9UI(frame9)
        # self.lab10UI(frame10)
        # self.lab11UI(frame11)
        # self.lab12UI(frame12)
        # self.lab13UI(frame13)
        
    def openBinaryFile(self):
            name = fd.askopenfilename() 
            self.currentData = self.inout.readFile(name)
    
    def openSoundFile(self):
        name = fd.askopenfilename() 
        self.currentSoundData = self.inout.readSoundFile(name)
    
    def saveBinaryFile(self):
        self.inout.saveFile(
            name = self.entryName.get(),
            data = self.currentData
        )
    
    def lab1UI(self, parent):
        Label(parent,
              text="Стандартные графики",
              font=self.font,
              ).pack(anchor=N, fill=X, pady=20)

        typeGraph = ["Восходящий", "Низходящий", "Восходящий и низходящий"]

        self.choseGraph1 = StringVar(value=0)
                
        for index in range(len(typeGraph)):
            radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseGraph1)
            radiobtn_graph.pack(anchor=N)
        
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
        ).pack(anchor=N, fill=X, pady=[20, 0])

        Button(
            parent,
            text="Построить экспонентный тренд",
            command=lambda: self.model.drawExponentaTrend(
                alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseGraph1.get())
            )
        ).pack(anchor=N, fill=X)

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
        ).pack(anchor=N, fill=X, pady=[0, 20])
        
        text = "Выводит график выбранного тренда.\n"
        text += "Изменяемые параметры в настройках:\n"
        text += "Для линейного тренда y = ax + b\n"
        text += "Для экспонетного тренда y = beta * e ^ (-alpha * x)"
        
        Label(parent,
              text=text).pack(anchor=N, fill=X)
    
    # def lab2UI(self, parent):
    #     Label(parent,
    #           text="ШУМЫ"
    #           ).pack(anchor=N, fill=X, pady=20)

    #     Button(
    #         parent,
    #         text="Построить график шума на основе линейного конгруэнтного ПСЧ",
    #         command=lambda: self.model.drawMyRandomNoise(
    #             Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #             N=int(self.parametrs.GetParametr("Parametrs", "N"))
    #         )
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Построить график шума основанного на встроенном ПСЧ",
    #         command=lambda: self.model.drawRandomNoise(
    #             Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #             N=int(self.parametrs.GetParametr("Parametrs", "N"))
    #         )
    #     ).pack(anchor=N, fill=X)

    #     Button(
    #         parent,
    #         text="Построить график всех шумов",
    #         command=lambda: self.model.drawNoise(
    #             Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #             N=int(self.parametrs.GetParametr("Parametrs", "N"))
    #         )
    #     ).pack(anchor=N, fill=X, pady=[0, 20])    
        
    #     text = "Генерирует два вида шума:\n"
    #     text += "1) На основе встроенного рандомайзера\n"
    #     text += "2) На основе написаного рандомайзера на \nоснове линейного конгруэнтного ПСЧ\n\n"
    #     text += "Редактируемый параметр R - максимальное значение,\nкоторое может быть сгенирировано" 
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
          
    # def lab3UI(self, parent):
    #     Label(parent,
    #           text="СТАТИСТИКА"
    #           ).pack(anchor=N, fill=X, pady=20)
        
        
    #     typeGraph = ['Шум на основе встроенного генератора', 'Шум на основе написанного генератора']

    #     self.choseNoise = StringVar(value=0)

    #     for index in range(len(typeGraph)):
    #         radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseNoise)
    #         radiobtn_graph.pack(anchor=N)
       
    #     del typeGraph
        
    #     Button(
    #         parent,
    #         text='Расчитать статистику',
    #         command=self.printStatistic
    #     ).pack(anchor=N, fill=X, pady=20)

    #     result = f'Количество значенией:\n'
    #     result += f'Минимальное значение:\n'
    #     result += f'Максимальное значение:\n'
    #     result += f'Среднее значение:\n'
    #     result += f'Дисперсия:\n'
    #     result += f'Стандартное отклонение:\n'
    #     result += f'Ассиметрия:\n'
    #     result += f'Коэффицент ассиметрии:\n'
    #     result += f'Эксцесс:\n'
    #     result += f'Куртозис:\n'
    #     result += f'Средний квадрат:\n'
    #     result += f'Ср. квад. ошибка:\n\n'
        
    #     self.label_statistic = Label(parent, text=result)
    #     self.label_statistic.pack(anchor=N, fill=X, pady=[0, 20])
        
    #     text = "Рассчитывает статистику для шума\n\n"
    #     text += "Редактируемый параметр R - максимальное значение,\nкоторое может быть сгенирировано" 
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
    
    # def lab4UI(self, parent):
    #     Label(parent,
    #           text="СМЕЩЕНИЕ И ИМПУЛЬСЫ"
    #           ).pack(anchor=N, fill=X, pady=20)
        
    #     typeGraph = ['Линейный восходящий', 'Линейный низходящий', 'Экспонента восходящая', 'Экспонента низходящая']
    #     self.choseGraph2 = StringVar(value=0)

    #     for index in range(len(typeGraph)):
    #         radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseGraph2)
    #         radiobtn_graph.pack(anchor=N)
       
    #     del typeGraph
    
    #     Button(
    #         parent,
    #         text='Построить смещение на графике',
    #         command=self.drawShift
    #     ).pack(anchor=N, fill=X, pady=[20,0])
        
    #     Button(
    #         parent,
    #         text="Построить импульсы",
    #         command=lambda: self.model.drawImpulseNoise(
    #             R=int(self.parametrs.GetParametr("Parametrs", "R2")),
    #             Rs=int(self.parametrs.GetParametr("Parametrs", "R1"))
    #         )
    #     ).pack(anchor=N, fill=X, pady=[0, 20])
        
    #     text = "Отрисовывает смещеные переданные данные на указанном диапозоне\n"
    #     text += "Если диапазон не передан, то смещение идет по всем данным\n"
    #     text += "И выводит импульс на переданных данных\n\n"
    #     text += "Редактируемы параметры:\n"
    #     text += "shift - величина смещения\n"
    #     text += "from - индекс начала смещения\n"
    #     text += "to - индекс конца смещения\n"
    #     text += "R1 = минимальное значение импульса\n"
    #     text += "R2 = максимальное значение импульса"
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
    
    # def lab5UI(self, parent):
    #     Label(parent,
    #           text="ГАРМОНИКИ"
    #           ).pack(anchor=N, fill=X, pady=20)
    
    #     Button(
    #         parent,
    #         text='Вывести гармонический процесс',
    #         command=lambda: self.model.drawHarm(
    #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #             A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #             f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #             dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #             thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
    #         )
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text='Вывести гармонический процесс с суммой трех гармоник',
    #         command=lambda: self.model.draw3In1Harm(
    #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #             A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #             A1=float(self.parametrs.GetParametr("Parametrs", "A1")),
    #             A2=float(self.parametrs.GetParametr("Parametrs", "A2")),
    #             f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #             f1=float(self.parametrs.GetParametr("Parametrs", "f1")),
    #             f2=float(self.parametrs.GetParametr("Parametrs", "f2")),
    #             dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #         )
    #     ).pack(anchor=N, fill=X)

    #     Button(
    #         parent,
    #         text='Вывести гармонический процесс с повышением f0 с указанным шагом',
    #         command=lambda: self.model.drawHarms(
    #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #             A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #             f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #             dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #             step=float(self.parametrs.GetParametr("Parametrs", "step"))
    #         )
    #     ).pack(anchor=N, fill=X, pady=[0, 20])
        
    #     text = "Выводит различные графики гармоник\n\n"
    #     text += "Редактируемые параметры:\n"
    #     text += "y = A * sin(2 * pi * f * dt * x + thetta\n"
    #     text += "A0, A1, A2\n"
    #     text += "f0, f1, f2\n"
    #     text += "thetta\n"
    #     text += "dt\n"
    #     text += "step - для повышения f0\n"
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)

    # def lab6UI(self, parent):
    #     Label(parent,
    #           text="ГИСТАГРАМА"
    #     ).pack(anchor=N, fill=X, pady=20)
    
    #     typeGraph = ['Линейный тренд', 'Экспонентный тренд', 'Шум', 'Гармоника']

    #     self.choseHis = StringVar(value=0)

    #     for index in range(len(typeGraph)):
    #         radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseHis)
    #         radiobtn_graph.pack(anchor=N)
       
    #     del typeGraph
        
    #     Button(
    #         parent,
    #         text="Построить гистаграмму",
    #         command=self.drawHistogram
    #     ).pack(anchor=N, fill=X, pady=20)
        
    #     text = "Выводит гистаграму переданных данных\n\n"
    #     text += "Редактируемые параметры:\n"
    #     text += "M - количество разбиений"
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
    
    # def lab7UI(self, parent):
    #     Label(
    #         parent,
    #         text="АВТОКОРЯЛЛЯЦИЯ И ВЗАИМНОКОРРЕЛЯЦИОННАЯ ФУНКЦИИ"
    #     ).pack(anchor=N, fill=X, pady=20)
        
    #     typeGraph = ['Шум встроенный', 'Шум написанный', 'Гармоника', 'Линейный тренд', 'Экспонентный тренд']

    #     self.choseAuto = StringVar(value=0)

    #     for index in range(len(typeGraph)):
    #         radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseAuto)
    #         radiobtn_graph.pack(anchor=N)
       
    #     del typeGraph

    #     Button(
    #         parent,
    #         text="Построить график автокорялляции",
    #         command=self.drawAutoKor
    #     ).pack(anchor=N, fill=X, pady=[20, 0])

    #     Button(
    #         parent,
    #         text="Построить взаимокорреляционную функцию",
    #         command=self.drawTwoAutoKor
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Удалить смещение в данных",
    #         command=self.antiShift
    #     ).pack(anchor=N, fill=X, pady=[0, 20])
        
    #     typeGraph = ['Шум встроенный c импульсами', 'Гармоника c импульсами']
        
    #     self.choseImpulse = StringVar(value=0)

    #     for index in range(len(typeGraph)):
    #         radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseImpulse)
    #         radiobtn_graph.pack(anchor=N)
       
    #     del typeGraph
        
    #     Button(
    #         parent,
    #         text="Удалить неправдоподобных значений в данных",
    #         command=self.antiSpike
    #     ).pack(anchor=N, fill=X, pady=20)
        
    #     text = "Рассчитываем и отрисовываект график\n"
    #     text += "автокорреляцию и вазимнокорреляцию переданной функции\n\n"
        
    #     text += "Следующая функция, это удаление смещения в данных\n"
    #     text += "А также удаление импульсов на данных\n\n"
        
    #     text += "Редактируемые параметры:\n"
    #     text += "R - максимальное значение, которое может быть сгенирировано (шум)\n"
    #     text += "y = A * sin(2 * pi * f * dt * x + thetta\n"
    #     text += "A0\n"
    #     text += "f0\n"
    #     text += "thetta\n"
    #     text += "dt\n"
    #     text += "R1 = минимальное значение импульса\n"
    #     text += "R2 = максимальное значение импульса"

        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
        
    # def lab8UI(self, parent):
    #     Label(parent,
    #           text="СЛОЖЕНИЕ ДАННЫХ"
    #           ).pack(anchor=N, fill=X, pady=20)

    #     typeGraph = ["Линейный тренд + гармоника", "Экспонентный тренд + шум"]

    #     self.choseSum = StringVar(value=0)

    #     for index in range(len(typeGraph)):
    #         radiobtn_graph = ttk.Radiobutton(parent, text=typeGraph[index], value=index, variable=self.choseSum)
    #         radiobtn_graph.pack(anchor=N)
            
    #     del typeGraph
        
    #     Button(
    #         parent,
    #         text="Сложить данные",
    #         command=self.addModel
    #     ).pack(anchor=N, fill=X, pady=[20,0])
        
    #     Button(
    #         parent,
    #         text="Удаление линейного тренда",
    #         command=lambda: self.processing.antiTrendLinear(
    #                             a=float(self.parametrs.GetParametr("Parametrs", "a")),
    #                             b=float(self.parametrs.GetParametr("Parametrs", "b")),
    #                             A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                             f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                             dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #                             thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
    #                             N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                         )
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Удаление нелинейного тренда",
    #         command= lambda: self.processing.antiTrendNonLinear(
    #             data=self.model.getSumModel(
    #                     data1=self.model.getExponentaTrend(
    #                         N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                         alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
    #                         beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
    #                         type=0
    #                     ),
    #                     data2=self.model.getNoise(
    #                         N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                         Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                         type=1
    #                     )
    #             ),
    #             W=[
    #                 int(self.parametrs.GetParametr("Parametrs", "W1")),
    #                 int(self.parametrs.GetParametr("Parametrs", "W2")),
    #                 int(self.parametrs.GetParametr("Parametrs", "W3"))
    #             ]      
    #         )
    #     ).pack(anchor=N, fill=X, pady=[0, 20])  
        
    #     text = "Складывает передаваемые данные\n\n"
    #     text += "Редактируемые параметры:\n"
    #     text += "1) Линейный тренд\n"
    #     text += "2) Гармоника\n"
    #     text += "3) Экспонетный тренд\n"
    #     text += "4) Шум\n"       
    #     text += "W1-3 - размер скользящего окна"  
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
    
    # def lab9UI(self, parent):
    #     Label(parent, text="Спектры Фурье").pack(anchor=N, fill=X, pady=20)
    #     Button(
    #         parent,
    #         text="Расчитать для гармонического процесса",
    #         command= lambda : self.analysis.spectrFourier(
    #             data=self.model.getHarm(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                 f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                 dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #                 thetta=float(self.parametrs.GetParametr("Parametrs", "thetta"))
    #             ),
    #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #             L = [
    #                 int(self.parametrs.GetParametr("Parametrs", "L1")),
    #                 int(self.parametrs.GetParametr("Parametrs", "L2")),
    #                 int(self.parametrs.GetParametr("Parametrs", "L3"))
    #             ]
    #         )
    #     ).pack(anchor=N, fill=X) 
        
    #     Button(
    #         parent,
    #         text="Расчитать для полигармонического процесса",
    #         command= lambda : self.analysis.spectrFourier(
    #             data=self.model.getPolyHarm(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                 A1=float(self.parametrs.GetParametr("Parametrs", "A1")),
    #                 A2=float(self.parametrs.GetParametr("Parametrs", "A2")),
    #                 f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                 f1=float(self.parametrs.GetParametr("Parametrs", "f1")),
    #                 f2=float(self.parametrs.GetParametr("Parametrs", "f2")),
    #                 dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #             ),
    #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #             L = [
    #                 int(self.parametrs.GetParametr("Parametrs", "L1")),
    #                 int(self.parametrs.GetParametr("Parametrs", "L2")),
    #                 int(self.parametrs.GetParametr("Parametrs", "L3"))
    #             ]
    #         )
    #     ).pack(anchor=N, fill=X, pady=[0, 20])
        
    #     text = "Рассчитывает и выводит спектр Фурье для переданных данных\n\n"
    #     text += "Редактируемые параметры:\n"
    #     text += "L1-3 размеры прямоугольного окна"
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
    
    # def lab10UI(self, parent):
    #     Label(parent, text="Антишум").pack(anchor=N, fill=X, pady=20)
    #     Button(
    #         parent,
    #         text="Убрать шум",
    #         command = lambda : self.processing.AntiNoise(
    #             function=self.model.getDefaultNoise,
    #             stepM=int(self.parametrs.GetParametr("Parametrs", "stepM"))
    #         )
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Убрать шум на гармонике",
    #         command = lambda: self.processing.AntiNoise(
    #             function=self.model.getSumHarmNoise,
    #             stepM=int(self.parametrs.GetParametr("Parametrs", "stepM"))
    #         )
    #     ).pack(anchor=N, fill=X, pady=[0, 20])
        
    #     text = "Убирает шум, также убирает шум на гармонике\n\n"
    #     text += "Редактируемые параметры:\n"
    #     text += "1) Шум\n"
    #     text += "2) Гармоника"
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)

    # def lab11UI(self, parent):
    #     Label(
    #         parent,
    #         text="Отобразить данные из файла"
    #     ).pack(anchor=N, fill=X, pady=20)
        
        
    #     Button(
    #         parent,
    #         text='Открыть файл', 
    #         command=self.openfile
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text='Отрисовать данные',
    #         command=lambda: self.analysis.drawFileData(self.currentData)
    #     ).pack(anchor=N, fill=X)
        
    #     Label(parent, text="Сохранение текущих данных").pack(anchor=N, fill=X, pady=20)
        
    #     Label(parent, text="Название файла").pack(anchor=N, fill=X)
        
    #     self.entryName = Entry(parent, width=20, justify=CENTER)
    #     self.entryName.pack(anchor=N)
        
    #     Button(
    #         parent,
    #         text="Задать тестовые данные",
    #         command=self.testCurrentdata
    #     ).pack(anchor=N, fill=X, pady= [20, 0])
        
    #     Button(
    #         parent,
    #         text="Сохранить",
    #         command=self.savefile
    #     ).pack(anchor=N, fill=X, pady= [0, 30])
        
    #     Button(
    #         parent,
    #         text = "Мульти тренд-гармоника",
    #         command= lambda: self.model.drawMultiModel(
    #             data1 = self.model.getDefaultExponentaTrend(),
    #             data2= self.model.getDefaultHarm()
    #         )
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text = "Кардиограмма",
    #         command=lambda: self.model.Cardiograma()
    #     ).pack(anchor=N, fill=X)
        
    #     text = "Считывает файл и сохраняет его в переменую текущих данных\n"
    #     text += "После этого можно отобразить данные\n"
    #     text += "Также сохраняет текущие данные в указанный файл\n"
    #     text += "Считывание происходит по 4 байта, сразу в формат float\n"
    #     text += "Также происходит сохзранение\n\n"
        
    #     text += "Реализована функция умножения данных, \nа также отображение кардиограммы"
        
    #     Label(parent, text=text).pack(anchor=N, fill=X, pady=20)

    # def lab12UI(self, parent):
    #     Label(parent, text="Расчет импульсной реакции").pack(anchor=N, fill=X, pady=20)
        
    #     Button(
    #         parent,
    #         text="Рассчитать для ФНЧ",
    #         command= lambda: self.processing.lpf(True)
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Рассчитать для ФВЧ",
    #         command= lambda: self.processing.hpf(True)
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Рассчитать для ПФ",
    #         command= lambda: self.processing.bpf(True)
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Рассчитать для РФ",
    #         command= lambda: self.processing.bsf(True)
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Расчет частотной характеристики фильтров",
    #         command= lambda: self.processing.FilterFourier()
    #     ).pack(anchor=N, fill=X, pady=20)
        
    #     text = "Расчет имульсной реакции для различных фильтров\n"
    #     text += "ФНЧ, ФВЧ, ПФ, РФ\n\n"
    #     text += "И расчет частотной характеристики фильтров\n\n"
    #     text += "Редактируемые параметры:\n"
    #     text += "fc, fc1, fc2, dt, m"
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
    
    # def lab13UI(self, parent):
    #     Label(parent, text="Применение фильтров к текущим данным").pack(anchor=N ,fill=X, pady=20)
        
    #     Button(
    #         parent,
    #         text="Применить ФВЧ",
    #         command=lambda: self.processing.useFilter(self.currentData)
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Применить ФНЧ",
    #         command=lambda: self.processing.useFilter(self.currentData, 1)
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Применить ПФ",
    #         command=lambda: self.processing.useFilter(self.currentData, 2)
    #     ).pack(anchor=N, fill=X)
        
    #     Button(
    #         parent,
    #         text="Применить РФ",
    #         command=lambda: self.processing.useFilter(self.currentData, 3)
    #     ).pack(anchor=N, fill=X)
        
        
    #     Button(
    #         parent,
    #         text="Чтение файла формата .wav",
    #         command= self.openSoundFile
    #     ).pack(anchor=N, fill=X, pady=[20, 0])
        
    #     Button(
    #         parent,
    #         text="Отобразить данные из текущего звукового файла",
    #         command=lambda: self.analysis.drawSoundData(self.currentSoundData)
    #     ).pack(anchor=N, fill=X, pady=[0, 20])
        
    #     text = "Применяет ранее написанные фильтра для считаных данных\n"
    #     text += "Также реализована функция чтения из файла формата .wav"
        
    #     Label(parent, text=text).pack(anchor=N, fill=X)
    
    # def printStatistic(self):
    #     result = self.analysis.statistics(
    #         self.model.getNoise(
    #             Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #             type=int(self.choseNoise.get())
    #         )
    #     )
    #     result += '\n\n'
    #     result += self.analysis.stationarity(
    #         self.model.getNoise(
    #             Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #             type=int(self.choseNoise.get())
    #         )
    #     )
        
    #     self.label_statistic.configure(text=result)

    # def drawShift(self):
    #     if int(self.choseGraph2.get()) == 0:
    #         self.model.drawShiftData(
    #             data=self.model.getLinerTrend(
    #                 a=float(self.parametrs.GetParametr("Parametrs", "a")),
    #                 b=float(self.parametrs.GetParametr("Parametrs", "b")),
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 type=0
    #                 ),
    #             shift=float(self.parametrs.GetParametr("Parametrs", "Shift")),
    #             N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom")),
    #             N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
    #         )
    #     elif int(self.choseGraph2.get()) == 1:
    #         self.model.drawShiftData(
    #             data=self.model.getLinerTrend(
    #                 a=float(self.parametrs.GetParametr("Parametrs", "a")),
    #                 b=float(self.parametrs.GetParametr("Parametrs", "b")),
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 type=1
    #                 ),
    #             shift=float(self.parametrs.GetParametr("Parametrs", "Shift")),
    #             N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom")),
    #             N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
    #         )
    #     elif int(self.choseGraph2.get()) == 2:
    #         self.model.drawShiftData(
    #             data=self.model.getExponentaTrend(
    #                 alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
    #                 beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 type=0
    #                 ),
    #             shift=float(self.parametrs.GetParametr("Parametrs", "Shift")),
    #             N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom")),
    #             N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
    #         )
    #     elif int(self.choseGraph2.get()) == 3:
    #         self.model.drawShiftData(
    #             data=self.model.getExponentaTrend(
    #                 alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
    #                 beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 type=1
    #                 ),
    #             shift=float(self.parametrs.GetParametr("Parametrs", "Shift")),
    #             N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom")),
    #             N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
    #         )
    
    # def drawHistogram(self):
    #     if int(self.choseHis.get()) == 0:
    #         self.analysis.histograma(
    #             self.model.getLinerTrend(
    #                 a=float(self.parametrs.GetParametr("Parametrs", "a")),
    #                 b=float(self.parametrs.GetParametr("Parametrs", "b")),
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 type=0
    #             ),
    #             M= int(self.parametrs.GetParametr("Parametrs", "M"))
    #         )
    #     elif int(self.choseHis.get()) == 1:
    #         self.analysis.histograma(
    #             self.model.getExponentaTrend(
    #                 alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
    #                 beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 type=0
    #             ),
    #             M= int(self.parametrs.GetParametr("Parametrs", "M"))
    #         )
    #     elif int(self.choseHis.get()) == 2:
    #         self.analysis.histograma(
    #             self.model.getNoise(
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 type=0
    #             ),
    #             M= int(self.parametrs.GetParametr("Parametrs", "M"))
    #         )
    #     elif int(self.choseHis.get()) == 3:
    #         self.analysis.histograma(
    #             self.model.getHarm(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                 f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                 dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #                 thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
    #             ),
    #             M= int(self.parametrs.GetParametr("Parametrs", "M"))
    #         )
    
    # def drawAutoKor(self):
    #     if int(self.choseAuto.get()) == 0:
    #         self.analysis.acf(
    #             self.model.getNoise(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 type=0
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 1:
    #         self.analysis.acf(
    #             self.model.getNoise(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 type=1
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 2:
    #         self.analysis.acf(
    #             self.model.getHarm(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                 f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                 dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #                 thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 3:
    #         self.analysis.acf(
    #             self.model.getLinerTrend(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 a=float(self.parametrs.GetParametr("Parametrs", "a")),
    #                 b=float(self.parametrs.GetParametr("Parametrs", "b")),
    #                 type=0
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 4:
    #         self.analysis.acf(
    #             self.model.getExponentaTrend(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
    #                 beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
    #                 type=1
    #             )
    #         )
    
    # def drawTwoAutoKor(self):
    #     if int(self.choseAuto.get()) == 0:
    #         self.analysis.ccf(
    #             self.model.getNoise(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 type=0
    #             ),
    #             self.model.getNoise(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 type=0
    #             ),
    #         )
    #     elif int(self.choseAuto.get()) == 1:
    #         self.analysis.ccf(
    #             self.model.getNoise(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 type=1
    #             ),
    #             self.model.getNoise(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 type=1
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 2:
    #         self.analysis.ccf(
    #             self.model.getHarm(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                 f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                 dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #                 thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
    #             ),
    #             self.model.getHarm(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 A0=float(self.parametrs.GetParametr("Parametrs", "A1")),
    #                 f0=float(self.parametrs.GetParametr("Parametrs", "f1")),
    #                 dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #                 thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
    #             )
    #         )
    
    # def antiShift(self):
    #     if int(self.choseAuto.get()) == 0:
    #         self.processing.antiShift(
    #             self.model.getNoise(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 type=0
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 1:
    #         self.processing.antiShift(
    #             self.model.getNoise(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                 type=1
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 2:
    #         self.processing.antiShift(
    #             self.model.getHarm(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                 f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                 dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #                 thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 3:
    #         self.processing.antiShift(
    #             self.model.getLinerTrend(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 a=float(self.parametrs.GetParametr("Parametrs", "a")),
    #                 b=float(self.parametrs.GetParametr("Parametrs", "b")),
    #                 type=0
    #             )
    #         )
    #     elif int(self.choseAuto.get()) == 4:
    #         self.processing.antiShift(
    #             self.model.getExponentaTrend(
    #                 N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                 alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
    #                 beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
    #                 type=1
    #             )
    #         ) 
    
    # def antiSpike(self):
    #     if int(self.choseImpulse.get()) == 0:
    #         data = data=self.model.getNoise(
    #                     Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                     N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                     type=0
    #                 )
    #         self.processing.antiSpike(
    #             data=self.model.getImpulseNoise(
    #                 data=self.model.getNoise(
    #                     Range=int(self.parametrs.GetParametr("Parametrs", "R")),
    #                     N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                     type=0
    #                 )
    #             ),
    #             min = np.min(data),
    #             max = np.max(data)
    #         )
    #     elif int(self.choseImpulse.get()) == 1:
    #         data = data=self.model.getHarm(
    #                     N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                     A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                     f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                     dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #         )
    #         self.processing.antiSpike(
    #             data=self.model.getImpulseNoise(
    #                 data=self.model.getHarm(
    #                     N=int(self.parametrs.GetParametr("Parametrs", "N")),
    #                     A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
    #                     f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
    #                     dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
    #                     thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
    #                 )
    #             ),
    #             min = np.min(data),
    #             max = np.max(data)
    #         )
    
    # def addModel(self):
        # if int(self.choseSum.get()) == 0:
        #     self.model.addModel(
        #         data1=self.model.getLinerTrend(
        #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
        #             a=float(self.parametrs.GetParametr("Parametrs", "a")),
        #             b=float(self.parametrs.GetParametr("Parametrs", "b")),
        #             type=0
        #         ),
        #         data2=self.model.getHarm(
        #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
        #             A0=float(self.parametrs.GetParametr("Parametrs", "A0")),
        #             f0=float(self.parametrs.GetParametr("Parametrs", "f0")),
        #             dt=float(self.parametrs.GetParametr("Parametrs", "dt")),
        #             thetta=float(self.parametrs.GetParametr("Parametrs", "thetta")),
        #         )
        #     )
        # elif int(self.choseSum.get()) == 1:
        #     self.model.addModel(
        #         data1=self.model.getExponentaTrend(
        #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
        #             alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
        #             beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
        #             type=0
        #         ),
        #         data2=self.model.getNoise(
        #             N=int(self.parametrs.GetParametr("Parametrs", "N")),
        #             Range=int(self.parametrs.GetParametr("Parametrs", "R")),
        #             type=1
        #         )
        #     )
    
    
        
    