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
        analysis.add_command(label="Гистограмма текущих данных", command=lambda : self.analysis.histograma(self.currentData, draw=True))
        analysis.add_command(label="Корреляция текущих данных", command=lambda : self.analysis.acf(self.currentData))
        analysis.add_command(label="Взаимокорреляция текущих и временных данных", command=lambda : self.analysis.ccf(self.currentData, self.tempData))
        analysis.add_command(label="Амплитудный спектр Фурье", command=lambda : self.analysis.spectrFourier(self.currentData, draw=True))
        
        
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
        
        frame1.pack(fill=BOTH, expand=True)
        frame2.pack(fill=BOTH, expand=True)
        frame3.pack(fill=BOTH, expand=True)
        frame4.pack(fill=BOTH, expand=True)
        frame5.pack(fill=BOTH, expand=True)
        
        notebook.add(frame1, text="Станд. графики")
        notebook.add(frame2, text="Генератор шумов")
        notebook.add(frame3, text="Изменить данные")
        notebook.add(frame4, text="Фильтры")
        notebook.add(frame5, text="Примеры")
        
        self.standartFunctionUI(frame1)
        self.noiseGeneratorUI(frame2)
        self.changeCurrentDataUI(frame3)
        self.filterUI(frame4)
        self.exampleUI(frame5)
        
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
    
    
        Button(
            parent,
            text="Удалить смещение по всем данным",
            command=lambda : self.writeCurrentData(self.processing.antiShift(self.currentData, draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Удалить неправдоподобных значений в данных",
            command=lambda : self.writeCurrentData(self.processing.antiSpike(self.currentData, draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Сложить текущие и временные данные",
            command=lambda : self.writeCurrentData(self.model.sumGraph(self.currentData, self.tempData, draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20,0])
        
        Button(
            parent,
            text="Перемножить текущие и временные данные",
            command=lambda : self.writeCurrentData(self.model.multiGraph(self.currentData, self.tempData, draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)

        
        
        
    def filterUI(self, parent):
        Button(
            parent,
            text="Рассчитать для ФНЧ",
            command= lambda: self.processing.lpf(draw=True),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])

        Button(
            parent,
            text="Рассчитать для ФВЧ",
            command= lambda: self.processing.hpf(draw=True),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Рассчитать для ПФ",
            command= lambda: self.processing.bpf(draw=True),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Рассчитать для РФ",
            command= lambda: self.processing.bsf(draw=True),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Фурье для фильтров",
            command= lambda: self.processing.filterFourier(),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=20)
        
        Button(
            parent,
            text="Применить ФВЧ",
            command=lambda: self.processing.useFilter(self.currentData),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Применить ФНЧ",
            command=lambda: self.processing.useFilter(self.currentData, 1),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Применить ПФ",
            command=lambda: self.processing.useFilter(self.currentData, 2),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Применить РФ",
            command=lambda: self.processing.useFilter(self.currentData, 3),
            font=self.mainFont
        ).pack(anchor=N, fill=X)   
        
    
    def exampleUI(self, parent):    
        Button(
            parent,
            text="Убрать линейный тренд на синусойде",
            command=lambda : self.writeCurrentData(self.processing.antiTrendLinear(draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Убрать нелинейный тренд",
            command=lambda : self.writeCurrentData(self.processing.antiTrendNonLinear(self.currentData, draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Убрать шум",
            command=lambda : self.processing.antiNoise(function=self.model.defaultNoise),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Кардиограмма",
            command=lambda : self.writeCurrentData(self.model.cardiograma(draw=True)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])