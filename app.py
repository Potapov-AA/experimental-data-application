from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd 
from tkinter import font

import numpy as np

from image import Image, TransformImageData, AnalysisImageData, FilterImageData

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
        h = 900

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
        
        imageFrame3 = ttk.Frame(notebook)
        imageFrame3.pack(fill=BOTH, expand=True)
        
        imageFrame4 = ttk.Frame(notebook)
        imageFrame4.pack(fill=BOTH, expand=True)
        
        imageNotebook.add(self.imageFrame1, text="Работа с файлами и отображение")
        imageNotebook.add(imageFrame2, text="Трансформация изображения")
        imageNotebook.add(imageFrame3, text="Анализ изображения")
        imageNotebook.add(imageFrame4, text="Фильтрация изображения")
        
        self.image_open_save_show_UI(self.imageFrame1)
        self.image_transform_UI(imageFrame2)
        self.image_analysis_UI(imageFrame3)
        self.image_filters_UI(imageFrame4)
        
        # frame1 = ttk.Frame(notebook)
        # frame2 = ttk.Frame(notebook)
        # frame3 = ttk.Frame(notebook)
        # frame4 = ttk.Frame(notebook)
        # frame5 = ttk.Frame(notebook)
        
        # frame1.pack(fill=BOTH, expand=True)
        # frame2.pack(fill=BOTH, expand=True)
        # frame3.pack(fill=BOTH, expand=True)
        # frame4.pack(fill=BOTH, expand=True)
        # frame5.pack(fill=BOTH, expand=True)
        
        # notebook.add(frame1, text="Станд. графики")
        # notebook.add(frame2, text="Генератор шумов")
        # notebook.add(frame3, text="Изменить данные")
        # notebook.add(frame4, text="Фильтры")
        # notebook.add(frame5, text="Примеры")
        
        # self.standartFunctionUI(frame1)
        # self.noiseGeneratorUI(frame2)
        # self.changeCurrentDataUI(frame3)
        # self.filterUI(frame4)
        # self.exampleUI(frame5)
    
    
    def image_open_save_show_UI(self, parent):
        
        buttonFrame = Frame(parent)
        buttonFrame.pack(fill=X)
        
        Button(
            buttonFrame,
            text="Открыть изображение",
            command=self.open_image,
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[30, 30], padx=[100, 0])
        
        Button(
            buttonFrame,
            text="Сохранить изображение",
            command=lambda:self.save_image(index=int(self.indexSpinbox.get())),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[30, 30])
        
        Button(
            buttonFrame,
            text="Отобразить изображение",
            command=lambda: self.show_image(index=int(self.indexSpinbox.get())),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[30, 10], padx=[0, 100])
        
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
        ).pack(pady=[10, 10])
        
        Button(
            parent,
            text="Добавить новое изображение",
            command=lambda: self.add_new_image(),
            font=self.mainFont
        ).pack(pady=[0, 10])
        
    
    def image_transform_UI(self, parent):
        Button(
            parent,
            text="Приведение данных изображения к серому диапазону",
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
            width = 15,
            command=lambda:self.work_with_image(TransformImageData.shift_data_image, 
                                                int(self.parametrs.GetParametr("ImageParametrs", "shiftMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[245, 0])
        
        Button(
            shiftMultyFrame,
            text="Умножение",
            width = 15,
            command=lambda:self.work_with_image(TransformImageData.multi_data_image, 
                                                int(self.parametrs.GetParametr("ImageParametrs", "shiftMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 245])
        
        Label(
            parent,
            text="Изменение размера изображения"
        ).pack(pady=[30, 0])
        
        resizeFrameOne = Frame(parent)
        resizeFrameOne.pack(fill=X)
        
        Button(
            resizeFrameOne,
            text="Метод ближайщих соседей",
            width = 30,
            command=lambda:self.work_with_image(TransformImageData.resize_image_nearest_neighbors, 
                                                float(self.parametrs.GetParametr("ImageParametrs", "resizeMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[110, 0])
        
        Button(
            resizeFrameOne,
            text="Метод билинейной интерполяции",
            width = 30,
            command=lambda:self.work_with_image(TransformImageData.resize_image_binary_method, 
                                                float(self.parametrs.GetParametr("ImageParametrs", "resizeMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 110])
        
        resizeFrameTwo = Frame(parent)
        resizeFrameTwo.pack(fill=X)
        
        Button(
            resizeFrameTwo,
            text="Увеличить (Фурье)",
            width = 30,
            command=lambda:self.work_with_image(TransformImageData.resize_up_image_fourier, 
                                                float(self.parametrs.GetParametr("ImageParametrs", "resizeMultiImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[5, 0], padx=[110, 0])
        
        Button(
            resizeFrameTwo,
            text="Уменьшить (Фурье)",
            width = 30,
            command=lambda:self.work_with_image(TransformImageData.resize_up_image_fourier, 
                                                float(self.parametrs.GetParametr("ImageParametrs", "resizeMultiImage"))),
            font=self.mainFont,
            state='disabled'
        ).pack(side=LEFT, anchor=N, expand=True, pady=[5, 0], padx=[0, 110])
        
        Label(
            parent,
            text="Поворот изображения"
        ).pack(pady=[30, 0])
        
        rotateFrame = Frame(parent)
        rotateFrame.pack(fill=X)
        
        Button(
            rotateFrame,
            text="Налево",
            width = 10,
            command=lambda:self.work_with_image(TransformImageData.rotate_image_left),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[290, 0])
        
        Button(
            rotateFrame,
            text="Направо",
            width = 10,
            command=lambda:self.work_with_image(TransformImageData.rotate_image_right),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 290])
        
        Label(
            parent,
            text="Применить эффект"
        ).pack(pady=[30, 0])
        
        effectFrame = Frame(parent)
        effectFrame.pack(fill=X)
        
        Button(
            effectFrame,
            text="Негатив",
            width = 15,
            command=lambda:self.work_with_image(TransformImageData.do_negative),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[245, 0])
        
        Button(
            effectFrame,
            text="Черно-белое",
            width = 15,
            command=lambda:self.work_with_image(TransformImageData.do_black_and_white, 
                                                int(self.parametrs.GetParametr("ImageParametrs", "blackAndWhiteFactorImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 245])
        
        Label(
            parent,
            text="Применить преобразования"
        ).pack(pady=[30, 0])
        
        transformFrame = Frame(parent)
        transformFrame.pack(fill=X)
        
        Button(
            transformFrame,
            text="Гамма преобразование",
            width = 35,
            command=lambda:self.work_with_image(TransformImageData.do_gamma_transform, 
                                                float(self.parametrs.GetParametr("ImageParametrs", "cImage")),
                                                float(self.parametrs.GetParametr("ImageParametrs", "yImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[65, 0])
        
        Button(
            transformFrame,
            text="Логарифмическое преобразование",
            width = 35,
            command=lambda:self.work_with_image(TransformImageData.do_logarithm_transform, 
                                                float(self.parametrs.GetParametr("ImageParametrs", "cImage"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 65])
        
        Button(
            parent,
            text="Градиционное преобразование",
            width = 72,
            command=lambda:self.work_with_image(TransformImageData.do_gradient_transform),
            font=self.mainFont
        ).pack(pady=[5, 0])
        
        
        Label(
            parent,
            text="Вычитание из последнего изображения, изображение по заданному индексу"
        ).pack(pady=[30, 0])
        
        Button(
            parent,
            text="Произвести вычетание",
            command=lambda:self.work_with_image(TransformImageData.get_difference_between_images,
                                                paramOne=self.image.get_last_data()),
            font=self.mainFont
        ).pack( pady=[0, 0])

        Label(
            parent,
            text="Зашумление изображения"
        ).pack(pady=[30, 0])
        
        noizeFrame = Frame(parent)
        noizeFrame.pack(fill=X)
        
        Button(
            noizeFrame,
            text="Соль и перец",
            width = 20,
            command=lambda:self.work_with_image(TransformImageData.do_solid_and_peaper, 
                                                int(self.parametrs.GetParametr("ImageParametrs", "countBadPixekOnRow"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[200, 0])
        
        Button(
            noizeFrame,
            text="Рандом",
            width = 20,
            command=lambda:self.work_with_image(TransformImageData.do_random_noise, 
                                                int(self.parametrs.GetParametr("ImageParametrs", "noiseRange"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 200])
        
        Label(
            parent,
            text="Выделение контуров"
        ).pack(pady=[30, 0])
        
        Button(
            parent,
            text="СГЕНЕРИРОВАТЬ МНОЖЕСТВО ВАРИАНТОВ",
            width = 52,
            command=lambda:self.work_with_image(TransformImageData.show_all_contoures),
            font=self.mainFont
        ).pack(pady=[0, 5])
        
        contoursFrame = Frame(parent)
        contoursFrame.pack(fill=X)
        
        Button(
            contoursFrame,
            text="Частотными фильтрами (ФНЧ)",
            width = 25,
            command=lambda:self.work_with_image(TransformImageData.select_contours_freq_lpf_filters,
                                                paramOne=float(self.parametrs.GetParametr("ImageParametrs", "freqOne")),
                                                paramTwo=float(self.parametrs.GetParametr("ImageParametrs", "freqTwo"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[155, 0])
        
        Button(
            contoursFrame,
            text="Частотными фильтрами (ФВЧ)",
            width = 25,
            command=lambda:self.work_with_image(TransformImageData.select_contours_freq_hpf_filters,
                                                paramOne=float(self.parametrs.GetParametr("ImageParametrs", "freqOne")),
                                                paramTwo=float(self.parametrs.GetParametr("ImageParametrs", "freqTwo"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 155])
        
    
    def image_analysis_UI(self, parent):
        Label(
            parent,
            text="Гистограммы"
        ).pack(pady=[30, 0])
        
        histogramFrame = Frame(parent)
        histogramFrame.pack(fill=X)
        
        Button(
            histogramFrame,
            text="Классическая",
            width = 20,
            command=lambda:self.analysis_image(AnalysisImageData.classic_histogram),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[100, 0])
        
        Button(
            histogramFrame,
            text="В сером диапозон",
            width = 20,
            command=lambda: self.analysis_image(AnalysisImageData.classic_histogram_with_to_gray_diapason),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 0])
        
        Button(
            histogramFrame,
            text="Нормализованная",
            width = 20,
            command=lambda: self.analysis_image(AnalysisImageData.normalaized_histogram),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 100])
        
        Label(
            parent,
            text="CDF"
        ).pack(pady=[30, 0])
        
        Button(
            parent,
            text="Расчитать",
            command=lambda: self.analysis_image(AnalysisImageData.calculate_CDF),
            font=self.mainFont
        ).pack(pady=[0, 0])
        
        Label(
            parent,
            text="Работа с производными строк изображения"
        ).pack(pady=[30, 0])
        
        Button(
            parent,
            text="Расчитать производные",
            width = 42,
            command=lambda: self.analysis_image(AnalysisImageData.calculate_derivatives,
                                                paramOne = int(self.parametrs.GetParametr("ImageParametrs", "derivativesStep"))),
            font=self.mainFont
        ).pack(pady=[0, 0])
        
        correlationFrame = Frame(parent)
        correlationFrame.pack(fill=X)
        
        Button(
            correlationFrame,
            text="Автокорреляция",
            width = 20,
            command=lambda:self.analysis_image(AnalysisImageData.calculate_auto_correlation,
                                               paramOne = int(self.parametrs.GetParametr("ImageParametrs", "derivativesStep"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[5, 0], padx=[200, 0])
        
        Button(
            correlationFrame,
            text="Кросскореляция",
            width = 20,
            command=lambda:self.analysis_image(AnalysisImageData.calculate_cross_correlation,
                                               paramOne = int(self.parametrs.GetParametr("ImageParametrs", "derivativesStep"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[5, 0], padx=[0, 200])
        
        Button(
            parent,
            text="Расчитать амплитудный спектр Фурье",
            width = 42,
            command=lambda: self.analysis_image(AnalysisImageData.calculate_fourier_transform,
                                                paramOne = int(self.parametrs.GetParametr("ImageParametrs", "derivativesStep"))),
            font=self.mainFont
        ).pack(pady=[0, 0])

        
        ### ТЕСТ ФУНКЦИИ ДЛЯ 1D ОБРАТНОГО ФУРЬЕ ###
        # Label(
        #     parent,
        #     text="Обратный Фурье 1D"
        # ).pack(pady=[30, 0])
        
        # Button(
        #     parent,
        #     text="Демонстрация",
        #     command=lambda: self.analysis_image(AnalysisImageData.inverse_fourier_transform_test_function),
        #     font=self.mainFont
        # ).pack(pady=[0, 0])
        ############################################
        
        Label(
            parent,
            text="2D преобразования Фурье"
        ).pack(pady=[30, 0])
        
        fourierFrame = Frame(parent)
        fourierFrame.pack(fill=X)
        
        Button(
            fourierFrame,
            text="Прямое",
            width = 15,
            command=lambda: self.analysis_image(AnalysisImageData.calculate_2D_fourier_transform, mode=1),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[245, 0])
        
        Button(
            fourierFrame,
            text="Обратное",
            width = 15,
            command=lambda: self.analysis_image(AnalysisImageData.calculate_inverse_2D_fourier_transform, mode=1),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 245])
        
    
    def image_filters_UI(self, parent):
        Label(
            parent,
            text="Фильтры Поттера"
        ).pack(pady=[30, 0])
        
        filtersPotterFrameOne = Frame(parent)
        filtersPotterFrameOne.pack(fill=X)
        
        Button(
            filtersPotterFrameOne,
            text="Фильтр низких частот",
            width = 20,
            command=lambda:self.filter_image(FilterImageData.lpf,
                                               paramOne=float(self.parametrs.GetParametr("ImageParametrs", "freqOne")),
                                               paramTwo=int(self.parametrs.GetParametr("ImageParametrs", "m"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[200, 0])
        
        Button(
            filtersPotterFrameOne,
            text="Фильтр высоких частот",
            width = 20,
            command=lambda:self.filter_image(FilterImageData.hpf,
                                               paramOne=float(self.parametrs.GetParametr("ImageParametrs", "freqOne")),
                                               paramTwo=int(self.parametrs.GetParametr("ImageParametrs", "m"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[0, 0], padx=[0, 200])
        
        filtersPotterFrameTwo = Frame(parent)
        filtersPotterFrameTwo.pack(fill=X)
        
        Button(
            filtersPotterFrameTwo,
            text="Полосовой фильтр",
            width = 20,
            command=lambda:self.filter_image(FilterImageData.bpf,
                                               paramOne=float(self.parametrs.GetParametr("ImageParametrs", "freqOne")),
                                               paramTwo=float(self.parametrs.GetParametr("ImageParametrs", "freqOne")),
                                               paramThree=int(self.parametrs.GetParametr("ImageParametrs", "m"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[5, 0], padx=[200, 0])
        
        Button(
            filtersPotterFrameTwo,
            text="Режекторный фильтр",
            width = 20,
            command=lambda:self.filter_image(FilterImageData.bsw,
                                               paramOne=float(self.parametrs.GetParametr("ImageParametrs", "freqOne")),
                                               paramTwo=float(self.parametrs.GetParametr("ImageParametrs", "freqOne")),
                                               paramThree=int(self.parametrs.GetParametr("ImageParametrs", "m"))),
            font=self.mainFont
        ).pack(side=LEFT, anchor=N, expand=True, pady=[5, 0], padx=[0, 200])
        
        Label(
            parent,
            text="Усредняющий арифметический фильтр"
        ).pack(pady=[30, 0])
        
        Button(
            parent,
            text="Применить",
            width = 15,
            command=lambda:self.filter_image(FilterImageData.middle_filter,
                                               paramOne=int(self.parametrs.GetParametr("ImageParametrs", "maskSize"))),
            font=self.mainFont
        ).pack(pady=[0, 0])
        
        Label(
            parent,
            text="Медианный фильтр"
        ).pack(pady=[30, 0])
        
        Button(
            parent,
            text="Применить",
            width = 15,
            command=lambda:self.filter_image(FilterImageData.median_filter,
                                               paramOne=int(self.parametrs.GetParametr("ImageParametrs", "maskSize"))),
            font=self.mainFont
        ).pack(pady=[0, 0])
        
        
        
    
    def work_with_image(self, function, paramOne=None, paramTwo=None):
        if int(self.indexSpinbox.get()) == -1:
            data = self.image.get_last_data()
        else:
            data = self.image.dataImageList[int(self.indexSpinbox.get())]
        
        if type(paramOne) is np.ndarray :
            transofrmData = function(TransformImageData(), data, paramOne)
        elif paramOne == None and paramTwo == None:
            transofrmData = function(TransformImageData(), data)
        elif paramTwo == None:
            transofrmData = function(TransformImageData(), data, paramOne)
        else:
            transofrmData = function(TransformImageData(), data, paramOne, paramTwo)
        
        self.image.add_updated_data_to_list(transofrmData)
        
        self.__reset_spinbox_count_images()
        
    
    def analysis_image(self, function, paramOne=None, mode=-1):
        if int(self.indexSpinbox.get()) == -1:
            data = self.image.get_last_data()
        else:
            data = self.image.dataImageList[int(self.indexSpinbox.get())]

        if paramOne == None:
            transofrmData =  function(AnalysisImageData(), data)
        else:
            transofrmData =  function(AnalysisImageData(), data, paramOne)
        
        if mode != -1:
            self.image.add_updated_data_to_list(transofrmData)
            self.__reset_spinbox_count_images()
        
    
    def filter_image(self, function, paramOne=None, paramTwo=None, paramThree=None):
        if int(self.indexSpinbox.get()) == -1:
            data = self.image.get_last_data()
        else:
            data = self.image.dataImageList[int(self.indexSpinbox.get())]
        
        if paramOne == None and paramTwo == None and paramThree == None:
            transofrmData = function(FilterImageData(), data)
        elif paramTwo == None and paramThree == None:
            transofrmData = function(FilterImageData(), data, paramOne)
        elif paramThree == None:
            transofrmData = function(FilterImageData(), data, paramOne, paramTwo)
        else:
            transofrmData = function(FilterImageData(), data, paramOne, paramTwo, paramThree)
        
        self.image.add_updated_data_to_list(transofrmData)
        
        self.__reset_spinbox_count_images()
            
    def open_image(self):
        path = fd.askopenfilename(filetypes = (('JPG', '.jpg'), ('PNG', '.png'), ('XCR', '.xcr'), ('BIN', '.bin')))
        
        if path == '': 
            return
        
        self.image = Image(path, int(self.heightSpinbox.get()), int(self.weightSpinbox.get()))
        
        self.__reset_spinbox_count_images()
    
    
    def save_image(self, index):
        self.image.save_image(index)
    
    
    def show_image(self, index):
        self.image.show_image(index)
    
    
    def add_new_image(self):
        path = fd.askopenfilename(filetypes = (('JPG', '.jpg'), ('PNG', '.png'), ('XCR', '.xcr'), ('BIN', '.bin')))
        
        if path == '': 
            return
        
        self.image.add_new_image(path, int(self.heightSpinbox.get()), int(self.weightSpinbox.get()))
        
        self.__reset_spinbox_count_images()
    
    
    def __reset_spinbox_count_images(self):
        self.indexSpinbox.destroy()
        self.indexSpinbox = Spinbox(
            self.spinboxFrame,
            from_= -1,
            to= self.image.get_last_index()
        )
        self.indexSpinbox.pack(side=LEFT, anchor=N, expand=True, pady=[10, 20], padx=[0, 250])
    
    
    
    
    
    
        
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
    