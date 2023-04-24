from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd 
from tkinter import font

import numpy as np

from image import Image, TransformImageData

from settings import ParametrSettings
from model import Model
from analysis import Analysis
from processing import Processing
from config import Config
from inout import InOut



class App(Tk):
    def __init__(self):
        super().__init__()
        
        self.image = Image()
        
        
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
        self.tempImage = []
        
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
        
        image = ttk.Frame(notebook)
        image.pack(fill=BOTH, expand=True)
        
        notebook.add(image, text="РАБОТА С ИЗОБРАЖЕНИЯМИ")
        
        imageNotebook = ttk.Notebook(image)
        imageNotebook.pack(expand=True, fill=BOTH)   
        
        self.imageFrame1 = ttk.Frame(notebook)
        self.imageFrame1.pack(fill=BOTH, expand=True)
        
        imageFrame2 = ttk.Frame(notebook)
        imageFrame2.pack(fill=BOTH, expand=True)
        
        imageNotebook.add(self.imageFrame1, text="Работа с файлами и отображение")
        imageNotebook.add(imageFrame2, text="Трансформация изображения")
        
        self.image_open_save_show_UI(self.imageFrame1)
        self.image_transform_UI(imageFrame2)
        
        
        
        # frame1 = ttk.Frame(notebook)
        # frame2 = ttk.Frame(notebook)
        # frame3 = ttk.Frame(notebook)
        # frame4 = ttk.Frame(notebook)
        # frame5 = ttk.Frame(notebook)
        frame6 = ttk.Frame(notebook)
        frame7 = ttk.Frame(notebook)
        
        # frame1.pack(fill=BOTH, expand=True)
        # frame2.pack(fill=BOTH, expand=True)
        # frame3.pack(fill=BOTH, expand=True)
        # frame4.pack(fill=BOTH, expand=True)
        # frame5.pack(fill=BOTH, expand=True)
        frame6.pack(fill=BOTH, expand=True)
        frame7.pack(fill=BOTH, expand=True)
        
        # notebook.add(frame1, text="Станд. графики")
        # notebook.add(frame2, text="Генератор шумов")
        # notebook.add(frame3, text="Изменить данные")
        # notebook.add(frame4, text="Фильтры")
        # notebook.add(frame5, text="Примеры")
        notebook.add(frame6, text="Работа с изображениями 1")
        notebook.add(frame7, text="Работа с изображениями 2")
        
        # self.standartFunctionUI(frame1)
        # self.noiseGeneratorUI(frame2)
        # self.changeCurrentDataUI(frame3)
        # self.filterUI(frame4)
        # self.exampleUI(frame5)
        self.imageUI_1(frame6)
        self.imageUI_2(frame7)
    
    
    def image_open_save_show_UI(self, parent):
        
        buttonFrame = Frame(parent)
        buttonFrame.pack(fill=X)
        
        Button(
            buttonFrame,
            text="Открыть изображение",
            command=self.open_image,
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[100, 30], padx=[100, 0])
        
        Button(
            buttonFrame,
            text="Сохранить изображение",
            command=lambda:self.save_image(index=int(self.indexSpinbox.get())),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[100, 30])
        
        Button(
            buttonFrame,
            text="Отобразить изображение",
            command=lambda: self.show_image(index=int(self.indexSpinbox.get())),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[100, 10], padx=[0, 100])
        
        spinboxsFrame = Frame(parent)
        spinboxsFrame.pack(fill=X)
        
        Label(
            spinboxsFrame,
            text="Высота и ширина изображения для xcr/bin"
        ).pack(side=LEFT, anchor=N, expand=True, pady=[5, 0], padx=[100, 0])
        
        self.heightSpinbox = Spinbox(
            spinboxsFrame,
            from_= 0,
            to= 4000
        )
        self.heightSpinbox.pack(side=LEFT, anchor=N, expand=True, pady=[5, 0])
        
        self.weightSpinbox = Spinbox(
            spinboxsFrame,
            from_= 0,
            to= 4000
        )
        self.weightSpinbox.pack(side=LEFT, anchor=N, expand=True, pady=[5, 0], padx=[0, 100])
        
        
        self.spinboxFrame = Frame(parent)
        self.spinboxFrame.pack(fill=X)
        
        Label(
            self.spinboxFrame,
            text="Индекс изображения"
        ).pack(side=LEFT, anchor=N, expand=True, pady=[10, 20], padx=[250, 0])
        
        self.indexSpinbox = Spinbox(
            self.spinboxFrame,
            from_= -1,
            to= self.image.get_last_index()
        )
        self.indexSpinbox.pack(side=LEFT, anchor=N, expand=True, pady=[10, 20], padx=[0, 250])
        
        Button(
            parent,
            text="Отобразить все изображения",
            command=lambda: self.image.show_all_images(),
            font=self.mainFont
        ).pack(pady=[0, 10])
        
    
    def image_transform_UI(self, parent):
        Button(
            parent,
            text="Приведение данныех изображения к серому диапазону",
            command=lambda:self.work_with_image(TransformImageData.data_to_gray_diapason),
            font=self.mainFont
        ).pack(pady=[30, 0])
        
        Label(
            parent,
            text="Смещение/Умножение данных изображения"
        ).pack(pady=[30, 0])
        
        shiftMultyFrame = Frame(parent)
        shiftMultyFrame.pack(fill=X)
        
        Button(
            shiftMultyFrame,
            text="Смещение",
            command=lambda:self.work_with_image(TransformImageData.shift_data_image, int(self.parametrs.GetParametr("ImageParametrs", "shiftMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[10, 0], padx=[290, 0])
        
        Button(
            shiftMultyFrame,
            text="Умножение",
            command=lambda:self.work_with_image(TransformImageData.multi_data_image, int(self.parametrs.GetParametr("ImageParametrs", "shiftMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[10, 0], padx=[0, 290])
        
        Label(
            parent,
            text="Изменение размера изображения"
        ).pack(pady=[30, 0])
        
        resizeFrame = Frame(parent)
        resizeFrame.pack(fill=X)
        
        Button(
            resizeFrame,
            text="Метод ближайщих соседей",
            command=lambda:self.work_with_image(TransformImageData.resize_image_nearest_neighbors, float(self.parametrs.GetParametr("ImageParametrs", "resizeMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[10, 0], padx=[150, 0])
        
        Button(
            resizeFrame,
            text="Метод билинейной интерполяции",
            command=lambda:self.work_with_image(TransformImageData.resize_image_binary_method, float(self.parametrs.GetParametr("ImageParametrs", "resizeMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[10, 0], padx=[0, 150])
        
    
    def work_with_image(self, function, param=-1):
        if param == -1:
            transofrmData = function(self, self.image.get_last_data())
        else:
            transofrmData = function(self, self.image.get_last_data(), param)
        
        self.image.add_updated_data_to_list(transofrmData)
        
        self.indexSpinbox.destroy()
        self.indexSpinbox = Spinbox(
            self.spinboxFrame,
            from_= -1,
            to= self.image.get_last_index()
        )
        self.indexSpinbox.pack(side=LEFT, anchor=N, expand=True, pady=[10, 20], padx=[0, 250])
        
    
    def open_image(self):
        path = fd.askopenfilename(filetypes = (('JPG', '.jpg'), ('PNG', '.png'), ('XCR', '.xcr'), ('BIN', '.bin')))
        
        if path == '': 
            return
        
        self.image = Image(path, int(self.heightSpinbox.get()), int(self.weightSpinbox.get()))
        
        self.indexSpinbox.destroy()
        self.indexSpinbox = Spinbox(
            self.spinboxFrame,
            from_= -1,
            to= self.image.get_last_index()
        )
        self.indexSpinbox.pack(side=LEFT, anchor=N, expand=True, pady=[10, 20], padx=[0, 250])
    
    
    def save_image(self, index):
        self.image.save_image(index)
    
    
    def show_image(self, index):
        self.image.show_image(index)
    
    
    
    
    
    
    
    
    
    
        
    def openBinaryFile(self):
        name = fd.askopenfilename() 
        self.currentData = self.inout.readBinaryFile(name)
    
    def openSoundFile(self):
        name = fd.askopenfilename() 
        self.currentSoundData = self.inout.readSoundFile(name)

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
    
    def writeCurrentImageDataInTemp(self):
        try:
            self.tempImage = self.currentImage
        except:
            print("Текущих данных не существует")
    
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
            command= lambda: self.processing.NewHPF(draw=True),
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
    
    
    def imageUI_1(self, parent):        
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
        
        Button(
            parent,
            text="Гистограмма текущего изображения",   
            command=lambda:self.analysis.ImageHistogram(self.currentImage),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Гистограмма текущего изображения с приведением к серому",   
            command=lambda:self.analysis.ImageHistogramWithToGray(self.currentImage),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="RGB гистограмма текущего изображения",   
            command=lambda:self.analysis.ImageRGBHistogram(self.currentImage),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Градиционное преобразование",   
            command=lambda:self.writeCurrentImageData(self.processing.ImageGradientTransform(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Сравнение изображений",   
            command=lambda:self.writeCurrentImageData(self.analysis.ResidualBetweenImages(self.currentImage, self.tempImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Применить фильтр Гарри Поттера",   
            command=lambda:self.writeCurrentImageData(self.processing.ResultForLab5(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
    
    def imageUI_2(self, parent):
        Button(
            parent,
            text="Посолить и поперчить изображение",   
            command=lambda:self.writeCurrentImageData(self.model.ToSolidAndPeaper(self.currentImage, n = 30)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Прорандомить изображение",   
            command=lambda:self.writeCurrentImageData(self.model.ToRandomNoise(self.currentImage, scale = 20)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Усредняющий арифметический фильтр",   
            command=lambda:self.writeCurrentImageData(self.processing.MiddleFilter(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Медианный фильтр",   
            command=lambda:self.writeCurrentImageData(self.processing.MedianFilter(self.currentImage)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        Button(
            parent,
            text="Сгенерировать изображение",   
            command=lambda:self.writeCurrentImageData(self.processing.GenerateImageBlackAndWhiteSqard()),
            font=self.mainFont
        ).pack(anchor=N, fill=X, pady=[20, 0])
        
        Button(
            parent,
            text="Обратный Фурье",   
            command=lambda:self.writeCurrentImageData(self.processing.InverseFurie(self.currentImage, mode = 3)),
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        
        Button(
            parent,
            text="Тест старых функций",   
            command=self.TEST,
            font=self.mainFont
        ).pack(anchor=N, fill=X)
        
        
    def TEST(self):
        from image import Image
        
        path = fd.askopenfilename() 
        image = Image(path)
        image.save_last_image()
        
        
        
        
        
        
            


