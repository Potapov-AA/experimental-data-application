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
        self.parametrs = Config()
        self.parametrs.DownloadSettings()
        self.title("МОЭД")
        self.centerWindow()
        self.initUI()

    def centerWindow(self):
        w = 400
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

        Label(self,
              text="ТРЕНДЫ"
              ).grid(row=0, column=0, columnspan=3, sticky=E+W, padx=10, pady=10)

        typeGraph = ["Восходящий", "Низходящий", "Восходящий и низходящий"]

        self.choseGraph = StringVar(value=0)

        column = 0
        for index in range(len(typeGraph)):
            print(index)
            radiobtn_graph = ttk.Radiobutton(text=typeGraph[index], value=index, variable=self.choseGraph)
            radiobtn_graph.grid(row=1, column=column, padx=5)
            column += 1
        del column

        Button(
            self,
            text="Построить линейный тренд",
            command=lambda: self.model.drawLinerTrend(
                a=float(self.parametrs.GetParametr("Parametrs", "a")),
                b=float(self.parametrs.GetParametr("Parametrs", "b")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseGraph.get())
            )
        ).grid(row=2, column=0, columnspan=3, padx=10,  pady=10)

        Button(
            self,
            text="Построить экспонентный тренд",
            command=lambda: self.model.drawExponentaTrend(
                alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=int(self.choseGraph.get())
            )
        ).grid(row=3, column=0, columnspan=3, padx=10)

        Button(
            self,
            text="Вывести график всех трендов",
            command=lambda: self.model.drawTrend(
                a=float(self.parametrs.GetParametr("Parametrs", "a")),
                b=float(self.parametrs.GetParametr("Parametrs", "b")),
                alpha=float(self.parametrs.GetParametr("Parametrs", "alpha")),
                beta=float(self.parametrs.GetParametr("Parametrs", "beta")),
                N=int(self.parametrs.GetParametr("Parametrs", "N"))
            )
        ).grid(row=4, column=0, columnspan=3, padx=10,  pady=10)

    
    
    

    # def lab2UI(self, table_lab_2):
    #     Label(table_lab_2, text='R = ', width=5).place(x=25, y=20)
    #     self.entry_R = Entry(table_lab_2, width=5)
    #     self.entry_R.place(x=60, y=22)

    #     Label(table_lab_2, text='N = ', width=5).place(x=95, y=20)
    #     self.entry_N_Noise = Entry(table_lab_2, width=5)
    #     self.entry_N_Noise.place(x=130, y=22)

    #     Button(
    #         table_lab_2,
    #         text="Построить график шума встроенного линейного конгруэнтного ПСЧ",
    #         command=self.drawMyRandomNoise
    #     ).place(x=25, y=50)

    #     Button(
    #         table_lab_2,
    #         text="Построить график шума основанного на встроенном ПСЧ",
    #         command=self.drawRandomNoise
    #     ).place(x=25, y=80)

    #     Button(
    #         table_lab_2,
    #         text="Построить график всех шумов",
    #         command=self.drawAllNoise
    #     ).place(x=25, y=110)

    # def lab3UI(self, table_lab_3):
    #     Label(table_lab_3, text='Выбирите график', width=15).place(x=25, y=20)
    #     self.combobox_chose_to_statistic = ttk.Combobox(table_lab_3)
    #     self.combobox_chose_to_statistic['values'] = (
    #         'Шум на основе встроенного генератора',
    #         'Шум на основе написанного генератора'
    #     )
    #     self.combobox_chose_to_statistic.current(0)
    #     self.combobox_chose_to_statistic.place(x=140, y=21)

    #     Label(table_lab_3, text='N = ', width=5).place(x=290, y=20)
    #     self.entry_N_statistic = Entry(table_lab_3, width=10)
    #     self.entry_N_statistic.place(x=325, y=21)

    #     Button(
    #         table_lab_3,
    #         text='Расчитать статистику',
    #         command=self.printStatistic
    #     ).place(x=25, y=60)

    #     self.label_statistic = Label(table_lab_3, text='')
    #     self.label_statistic.place(x=150, y=100)

    # def lab4UI(self, table_lab_4):
    #     self.combobox_chose_to_shift = ttk.Combobox(table_lab_4)
    #     self.combobox_chose_to_shift['values'] = (
    #         'Линейный восходящий',
    #         'Линейный низходящий',
    #         'Экспонента восходящая',
    #         'Экспонента низходящая'
    #     )
    #     self.combobox_chose_to_shift.current(0)
    #     self.combobox_chose_to_shift.place(x=25, y=20)

    #     Label(table_lab_4, text='Смещение =', width=10).place(x=180, y=20)
    #     self.entry_shift = Entry(table_lab_4, width=5)
    #     self.entry_shift.place(x=260, y=22)

    #     Label(table_lab_4, text='От', width=5).place(x=300, y=20)
    #     self.entry_N1_shift = Entry(table_lab_4, width=5)
    #     self.entry_N1_shift.place(x=340, y=22)

    #     Label(table_lab_4, text='До', width=5).place(x=370, y=20)
    #     self.entry_N2_shift = Entry(table_lab_4, width=5)
    #     self.entry_N2_shift.place(x=410, y=22)

    #     Label(table_lab_4, text='N =', width=5).place(x=25, y=80)
    #     self.entry_N_impulse = Entry(table_lab_4, width=5)
    #     self.entry_N_impulse.place(x=60, y=82)

    #     Label(table_lab_4, text='R =', width=5).place(x=90, y=80)
    #     self.entry_R_impulse = Entry(table_lab_4, width=5)
    #     self.entry_R_impulse.place(x=125, y=82)

    #     Label(table_lab_4, text='Rs =', width=5).place(x=160, y=80)
    #     self.entry_Rs_impulse = Entry(table_lab_4, width=5)
    #     self.entry_Rs_impulse.place(x=200, y=82)

    #     Button(
    #         table_lab_4,
    #         text='Построить смещение на графике',
    #         command=self.drawShift
    #     ).place(x=25, y=50)

    #     Button(
    #         table_lab_4,
    #         text="Построить импульсы",
    #         command=self.drawImpulse
    #     ).place(x=25, y=110)

    # def lab5UI(self, table_lab_5):
    #     Label(table_lab_5, text='N =', width=5).place(x=25, y=20)
    #     self.entry_N_harmonic = Entry(table_lab_5, width=5)
    #     self.entry_N_harmonic.place(x=60, y=21)

    #     Label(table_lab_5, text='A0 =', width=5).place(x=100, y=20)
    #     self.entry_A0 = Entry(table_lab_5, width=5)
    #     self.entry_A0.place(x=135, y=21)

    #     Label(table_lab_5, text='A1 =', width=5).place(x=100, y=45)
    #     self.entry_A1 = Entry(table_lab_5, width=5)
    #     self.entry_A1.place(x=135, y=46)

    #     Label(table_lab_5, text='A2 =', width=5).place(x=100, y=70)
    #     self.entry_A2 = Entry(table_lab_5, width=5)
    #     self.entry_A2.place(x=135, y=71)

    #     Label(table_lab_5, text='f0 =', width=5).place(x=170, y=20)
    #     self.entry_f0 = Entry(table_lab_5, width=5)
    #     self.entry_f0.place(x=205, y=21)

    #     Label(table_lab_5, text='f1 =', width=5).place(x=170, y=45)
    #     self.entry_f1 = Entry(table_lab_5, width=5)
    #     self.entry_f1.place(x=205, y=46)

    #     Label(table_lab_5, text='f0 =', width=5).place(x=170, y=70)
    #     self.entry_f2 = Entry(table_lab_5, width=5)
    #     self.entry_f2.place(x=205, y=71)

    #     Label(table_lab_5, text='dt =', width=5).place(x=240, y=20)
    #     self.entry_dt = Entry(table_lab_5, width=5)
    #     self.entry_dt.place(x=275, y=21)

    #     Label(table_lab_5, text='thetta =', width=5).place(x=320, y=20)
    #     self.entry_tetta = Entry(table_lab_5, width=5)
    #     self.entry_tetta.place(x=365, y=21)

    #     Label(table_lab_5, text='step =', width=5).place(x=400, y=20)
    #     self.entry_step = Entry(table_lab_5, width=5)
    #     self.entry_step.place(x=440, y=21)

    #     Button(
    #         table_lab_5,
    #         text='Вывести гармонический процесс',
    #         command=self.drawHarmonic
    #     ).place(x=25, y=100)

    #     Button(
    #         table_lab_5,
    #         text='Вывести гармонический процесс с суммой трех гармоник',
    #         command=self.drawHarmonics
    #     ).place(x=25, y=130)

    #     Button(
    #         table_lab_5,
    #         text='Вывести гармонический процесс с повышением f0 с указанным шагом',
    #         command=self.drawSumHarmonics
    #     ).place(x=25, y=160)

    # def lab6UI(self, table_lab_5):
    #     pass

    

    # def drawAllNoise(self):
    #     Model().drawNoise(
    #         Range=float(self.entry_R.get()),
    #         N=int(self.entry_N_Noise.get())
    #     )

    # def drawMyRandomNoise(self):
    #     Model().drawMyRandomNoise(
    #         Range=float(self.entry_R.get()),
    #         N=int(self.entry_N_Noise.get())
    #     )

    # def drawRandomNoise(self):
    #     Model().drawRandomNoise(
    #         Range=float(self.entry_R.get()),
    #         N=int(self.entry_N_Noise.get())
    #     )

    # def drawShift(self):
    #     if self.combobox_chose_to_shift.get() == 'Линейный восходящий':
    #         Model().drawShiftData(
    #             data=Model().getLinerTrend(a=10, b=12, N=1000, type=1),
    #             shift=float(self.entry_shift.get()),
    #             N1=int(self.entry_N1_shift.get()),
    #             N2=int(self.entry_N2_shift.get())
    #         )
    #     elif self.combobox_chose_to_shift.get() == 'Линейный низходящий':
    #         Model().drawShiftData(
    #             data=Model().getLinerTrend(a=10, b=12, N=1000, type=2),
    #             shift=float(self.entry_shift.get()),
    #             N1=int(self.entry_N1_shift.get()),
    #             N2=int(self.entry_N2_shift.get())
    #         )
    #     elif self.combobox_chose_to_shift.get() == 'Экспонента восходящая':
    #         Model().drawShiftData(
    #             data=Model().getExponentaTrend(alpha=0.15, beta=10, N=1000, type=1),
    #             shift=float(self.entry_shift.get()),
    #             N1=int(self.entry_N1_shift.get()),
    #             N2=int(self.entry_N2_shift.get())
    #         )
    #     elif self.combobox_chose_to_shift.get() == 'Экспонента низходящая':
    #         Model().drawShiftData(
    #             data=Model().getExponentaTrend(alpha=0.15, beta=10, N=1000, type=2),
    #             shift=float(self.entry_shift.get()),
    #             N1=int(self.entry_N1_shift.get()),
    #             N2=int(self.entry_N2_shift.get())
    #         )

    # def drawImpulse(self):
    #     Model().drawImpulseNoise(
    #         N=int(self.entry_N_impulse.get()),
    #         R=int(self.entry_R_impulse.get()),
    #         Rs=int(self.entry_Rs_impulse.get())
    #     )

    # def printStatistic(self):
    #     if self.combobox_chose_to_statistic.get() == 'Шум на основе встроенного генератора':
    #         result = Analysis().statistics(Model().getNoise(
    #             100, int(self.entry_N_statistic.get()), 1))
    #         result += '\n\n'
    #         result += Analysis().stationarity(Model().getNoise(100,
    #                                                            int(self.entry_N_statistic.get()), 1))
    #         self.label_statistic.configure(text=result)
    #     elif self.combobox_chose_to_statistic.get() == 'Шум на основе написанного генератора':
    #         result = Analysis().statistics(Model().getNoise(
    #             100, int(self.entry_N_statistic.get()), 2))
    #         result += '\n\n'
    #         result += Analysis().stationarity(Model().getNoise(100,
    #                                                            int(self.entry_N_statistic.get()), 2))
    #         self.label_statistic.configure(text=result)

    # def drawHarmonic(self):
    #     Model().drawHarm(
    #         N=int(self.entry_N_harmonic.get()),
    #         A0=float(self.entry_A0.get()),
    #         f0=float(self.entry_f0.get()),
    #         dt=float(self.entry_dt.get()),
    #         thetta=float(self.entry_tetta.get())
    #     )

    # def drawHarmonics(self):
    #     Model().drawHarms(
    #         N=int(self.entry_N_harmonic.get()),
    #         A0=float(self.entry_A0.get()),
    #         f0=float(self.entry_f0.get()),
    #         dt=float(self.entry_dt.get()),
    #         step=int(self.entry_step.get())
    #     )

    # def drawSumHarmonics(self):
    #     Model().draw3In1Harm(
    #         N=int(self.entry_N_harmonic.get()),
    #         A0=float(self.entry_A0.get()),
    #         A1=float(self.entry_A1.get()),
    #         A2=float(self.entry_A2.get()),
    #         f0=float(self.entry_f0.get()),
    #         f1=float(self.entry_f1.get()),
    #         f2=float(self.entry_f2.get()),
    #         dt=float(self.entry_dt.get())
    #     )
