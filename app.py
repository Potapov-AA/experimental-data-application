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
        self.tempSoundData = []
        
        self.currentFilter = []
        self.currentFilterSound = []

        self.currentImage = []
        
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
        filemenu.add_command(label="Сохранить текущий файл с данными", command=lambda : self.inout.saveBinaryFile("saveData/data.bin", self.currentData))
        
        filemenu.add_command(label="Записать текущие данные во временную переменную", command=self.writeCurrentDataInTemp)
        
        filemenu.add_command(label="Открыть звуковой файл", command=self.openSoundFile)
        filemenu.add_command(label="Отобразить текущие звуковые данные", command=lambda : self.model.drawSoundData(self.currentSoundData))
        filemenu.add_command(label="Сохранить текущие звуковые данные", command=lambda : self.inout.saveSoundFile("saveData/data.wav", self.currentSoundData))
        
        filemenu.add_command(label="Открыть изображение", command=self.openImageFile)
        filemenu.add_command(label="Открыть изображение из .xcr", command=self.openXcrFile)
        filemenu.add_command(label="Открыть изображение из .bin", command=self.openBinFile)
        filemenu.add_command(label="Отобразить текущее изображение", command=lambda : self.model.drawImageData(self.currentImage))
        filemenu.add_command(label="Сохранить текущее изображение", command=lambda : self.inout.saveImage("saveData/img.jpg", self.currentImage))
        filemenu.add_command(label="Сохранить текущее изображение в .bin", command=lambda : self.inout.saveBinImages("saveData/img.bin", self.currentImage))
        
        filemenu.add_command(label="Записать выбранный фрагмент звуковых данных во временную переменную", command=self.writeCurrentSoundDataInTemp)
        filemenu.add_command(label="Отобразить выбранный фрагмент звуковых данных", command=lambda : self.model.drawData(self.tempSoundData))
        
        filemenu.add_command(label="Выход", command=self.destroy)
        

        settings = Menu(mainmenu, tearoff=0)
        settings.add_command(label="Настройки параметров", command=self.openParametrSettings)
        
        
        analysis = Menu(mainmenu, tearoff=0)
        analysis.add_command(label="Сохранить статистику текущих данных", command=self.statisticCurrentFile)
        analysis.add_command(label="Гистограмма текущих данных", command=lambda : self.analysis.histograma(self.currentData, draw=True))
        analysis.add_command(label="Корреляция текущих данных", command=lambda : self.analysis.acf(self.currentData))
        analysis.add_command(label="Взаимокорреляция текущих и временных данных", command=lambda : self.analysis.ccf(self.currentData, self.tempData))
        analysis.add_command(label="Амплитудный спектр Фурье", command=lambda : self.analysis.spectrFourier(self.currentData, draw=True))
        analysis.add_command(label="Амплитудный спектр Фурье для аудиофрагмента", command=lambda : self.analysis.spectrFourierForAudio(self.tempSoundData, rate=self.currentSoundData["framerate"], draw=True))
        
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
        
        frame1.pack(fill=BOTH, expand=True)
        frame2.pack(fill=BOTH, expand=True)
        frame3.pack(fill=BOTH, expand=True)
        frame4.pack(fill=BOTH, expand=True)
        frame5.pack(fill=BOTH, expand=True)
        frame6.pack(fill=BOTH, expand=True)
        
        notebook.add(frame1, text="Станд. графики")
        notebook.add(frame2, text="Генератор шумов")
        notebook.add(frame3, text="Изменить данные")
        notebook.add(frame4, text="Фильтры")
        notebook.add(frame5, text="Примеры")
        notebook.add(frame6, text="Работа с изображениями")
        
        self.standartFunctionUI(frame1)
        self.noiseGeneratorUI(frame2)
        self.changeCurrentDataUI(frame3)
        self.filterUI(frame4)
        self.exampleUI(frame5)
        self.imageUI(frame6)
     
        
    def openBinaryFile(self):
        name = fd.askopenfilename() 
        self.currentData = self.inout.readBinaryFile(name)
    
    def openSoundFile(self):
        name = fd.askopenfilename() 
        self.currentSoundData = self.inout.readSoundFile(name)
    
    def openImageFile(self):
        name = fd.askopenfilename() 
        self.currentImage = self.inout.readImages(name)
    
    def openXcrFile(self):
        name = fd.askopenfilename() 
        self.currentImage = self.inout.readXcrImage(name)
        
    def openBinFile(self):
        name = fd.askopenfilename() 
        self.currentImage = self.inout.readBinImage(name)
        
    
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
    
    def writeCurrentSoundData(self, function):
        self.currentSoundData = function
    
    def writeCurrentImageData(self, function):
        self.currentImage = function
    
    def writeCurrentSoundDataInTemp(self):
        try:
            sN1=int(float(self.parametrs.GetParametr("Parametrs", "sN1")) * self.currentSoundData["framerate"])
            sN2=int(float(self.parametrs.GetParametr("Parametrs", "sN2")) * self.currentSoundData["framerate"])
            if sN1!=0 and sN2!=0:
                dataForAnalys = []
                for i in range(sN1, sN2):
                    dataForAnalys.append(self.currentSoundData["data"][i])
                self.tempSoundData = dataForAnalys
            else:
                self.tempSoundData = self.currentSoundData["data"]
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
        
        Button(
            parent,
            text="Поменять ударный слог",
            command=lambda : self.writeCurrentSoundData(self.processing.newStressedSyllable(self.currentSoundData)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20,0])

        
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
        
        
        Button(
            parent,
            text="Применить ФВЧ к звуковым данным",
            command=lambda: self.processing.useFilter(self.tempSoundData, sound=True),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Применить ФНЧ к звуковым данным",
            command=lambda: self.processing.useFilter(self.tempSoundData, 1, sound=True),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Применить ПФ к звуковым данным",
            command=lambda: self.processing.useFilter(self.tempSoundData, 2, sound=True),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Применить РФ к звуковым данным",
            command=lambda: self.processing.useFilter(self.tempSoundData, 3, sound=True),
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
    
    
    def imageUI(self, parent):
        Button(
            parent,
            text="Смещение данных изображения",
            command=lambda:self.writeCurrentImageData(self.processing.shift2D(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Умножение данных изображения на константу",
            command=lambda:self.writeCurrentImageData(self.processing.multModel2D(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Привести к серому цвету",
            command=lambda:self.writeCurrentImageData(self.processing.toGray(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Изменить размер изображения (ближайшие соседи)",
            command=lambda:self.writeCurrentImageData(self.processing.resizeNearestImage(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Изменить размер изображения (бинарный)",   
            command=lambda:self.writeCurrentImageData(self.processing.resizeBinaryImage(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Повернуть изображение налево",   
            command=lambda:self.writeCurrentImageData(self.processing.rotateImage(self.currentImage, False)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Повернуть изображение направо",   
            command=lambda:self.writeCurrentImageData(self.processing.rotateImage(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Сделать изображение негативным",   
            command=lambda:self.writeCurrentImageData(self.processing.doNegative(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Сделать изображение серым",   
            command=lambda:self.writeCurrentImageData(self.processing.doGray(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Гамма-преобразование",   
            command=lambda:self.writeCurrentImageData(self.processing.gammaTransform(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Логарифмическое преобразование",   
            command=lambda:self.writeCurrentImageData(self.processing.logTransform(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        
        
    def TEST(self):
        import PIL.Image as pil
        from matplotlib import pyplot as plt
        
        
        
        # plt.figure(figsize=(6,6))
        # plt.imshow(data_image)
        # plt.axis("off")
        # plt.show()
        