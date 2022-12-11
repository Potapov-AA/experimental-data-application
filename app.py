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
        self.tempData = []
        
        self.currentSoundData = []
        
        self.mainFont = font.Font(family="Time New Roman", size=12, weight="normal", slant="roman")
        
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
        
        filemenu.add_command(label="Отобразить текущие данные", command=lambda : self.model.drawData(self.currentData))
        filemenu.add_command(label="Сохранить текущий файл с данными", command=lambda : self.saveBinaryFile("saveData/data.bin"))
        
        filemenu.add_command(label="Записать текущие данные во временную переменную", command=self.writeCurrentDataInTemp)
        
        filemenu.add_command(label="Открыть звуковой файл", command=self.openSoundFile)
        filemenu.add_command(label="Отобразить текущие звуковые данные", command=lambda : self.model.drawCurrentSoundData(self.currentSoundData))
        
        filemenu.add_command(label="Выход", command=self.destroy)
        

        settings = Menu(mainmenu, tearoff=0)
        settings.add_command(label="Настройки параметров", command=self.openParametrSettings)
        
        
        analysis = Menu(mainmenu, tearoff=0)
        analysis.add_command(label="Сохранить статистику текущих данных", command=self.statisticCurrentFile)
        analysis.add_command(label="Гистограмма текущих данных", command=lambda : self.analysis.histograma(self.currentData))
        
        
        mainmenu.add_cascade(label="Файл", menu=filemenu)
        mainmenu.add_cascade(label="Анализ", menu=analysis)
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
        # frame6.pack(fill=BOTH, expand=True)
        # frame7.pack(fill=BOTH, expand=True)
        # frame8.pack(fill=BOTH, expand=True)
        # frame9.pack(fill=BOTH, expand=True)
        # frame10.pack(fill=BOTH, expand=True)
        # frame11.pack(fill=BOTH, expand=True)
        # frame12.pack(fill=BOTH, expand=True)
        # frame13.pack(fill=BOTH, expand=True)
        
        notebook.add(frame1, text="Станд. графики")
        notebook.add(frame2, text="Генератор шумов")
        notebook.add(frame3, text="Изменить данные")
        notebook.add(frame4, text="ы")
        notebook.add(frame5, text="Примеры")
        # notebook.add(frame6, text="Л. 6")
        # notebook.add(frame7, text="Л. 7")
        # notebook.add(frame8, text="Л. 8")
        # notebook.add(frame9, text="Л. 9")
        # notebook.add(frame10, text="Л. 10")
        # notebook.add(frame11, text="Л. 11")
        # notebook.add(frame12, text="Л. 12")
        # notebook.add(frame13, text="Л. 13")
        
        self.standartFunctionUI(frame1)
        self.noiseGeneratorUI(frame2)
        self.changeCurrentDataUI(frame3)
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
        self.currentData = self.inout.readBinaryFile(name)
    
    def openSoundFile(self):
        name = fd.askopenfilename() 
        self.currentSoundData = self.inout.readSoundFile(name)
    
    def saveBinaryFile(self, name):
        self.inout.saveBinaryFile(
            name = name,
            data = self.currentData
        )
    
    
    def statisticCurrentFile(self):
        statisticText = self.analysis.statistics(self.currentData)
        statisticText += '\n'
        statisticText += self.analysis.stationarity(self.currentData)
        
        self.inout.statisticSave("saveData/statistic.txt", statisticText)
    
    
    def writeCurrentData(self, function):
        self.currentData = function
    
    def writeCurrentDataInTemp(self):
        try:
            self.tempData = self.currentData
        except:
            print("Текущих данных не существует")
    
    
    def standartFunctionUI(self, parent):
        Button(
            parent,
            text="Построить линейный график",
            command=lambda : self.writeCurrentData(self.model.linerGraph(draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])

        Button(
            parent,
            text="Построить график экспоненты",
            command=lambda : self.writeCurrentData(self.model.exponentaGraph(draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
    
        Button(
            parent,
            text="Построить синусойду",
            command=lambda : self.writeCurrentData(self.model.sinGraph(draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)

        Button(
            parent,
            text='Построить сумму трех синусойд',
            command=lambda : self.writeCurrentData(self.model.sinSumGraph(draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)

        Button(
            parent,
            text='Вывести гармонический процесс с повышением f0 с шагом',
            command=self.model.drawSinWithStep,
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[0, 20])
        
    
    def noiseGeneratorUI(self, parent):
        Button(
            parent,
            text="Построить график шума на встроенном ПСЧ",
            command= lambda : self.writeCurrentData(self.model.defaultNoise(draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20,0])
        
        Button(
            parent,
            text="Построить график шума основанного на встроенном ПСЧ",
            command=lambda : self.writeCurrentData(self.model.lineKonNoise(draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
    
    
    def changeCurrentDataUI(self, parent):
        Button(
            parent,
            text='Сделать смещение на данных',
            command=lambda : self.writeCurrentData(self.model.shiftData(self.currentData, draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20,0])
        
        Button(
            parent,
            text="Сделать импульсы на данных",
            command=lambda : self.writeCurrentData(self.model.impulseData(self.currentData, draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
    

    
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
    
    
        
    