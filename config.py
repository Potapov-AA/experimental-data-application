import configparser
import os


class Config():
    def __init__(self):
        self.path = 'settings.ini'
        self.config = configparser.ConfigParser()

    def DownloadSettings(self):
        if not os.path.exists(self.path):
            self.DefaultSettings()

    def DefaultSettings(self):
        self.config.add_section("Parametrs")
        self.config.set("Parametrs", "N", "1000")
        self.config.set("Parametrs", "a", "1")
        self.config.set("Parametrs", "b", "1")
        self.config.set("Parametrs", "alpha", "0.01")
        self.config.set("Parametrs", "beta", "1")
        self.config.set("Parametrs", "R", "1000")
        self.config.set("Parametrs", "Shift", "500")
        self.config.set("Parametrs", "ShiftFrom", "0")
        self.config.set("Parametrs", "ShiftTo", "500")
        self.config.set("Parametrs", "R1", "500")
        self.config.set("Parametrs", "R2", "800")
        self.config.set("Parametrs", "A0", "100")
        self.config.set("Parametrs", "A1", "50")
        self.config.set("Parametrs", "A2", "25")
        self.config.set("Parametrs", "f0", "4")
        self.config.set("Parametrs", "f1", "1")
        self.config.set("Parametrs", "f2", "20")
        self.config.set("Parametrs", "dt", "0.001")
        self.config.set("Parametrs", "step", "250")
        self.config.set("Parametrs", "thetta", "0")
        self.config.set("Parametrs", "M", "100")
        self.config.set("Parametrs", "W1", "10")
        self.config.set("Parametrs", "W2", "15")
        self.config.set("Parametrs", "W3", "20")

        with open(self.path, "w") as configFiles:
            self.config .write(configFiles)

    def UpdateParametr(self, section, parametrName, value):
        self.config.set(section, parametrName, value)
        with open(self.path, "w") as configFiles:
            self.config.write(configFiles)

    def GetParametr(self, section, parametrName):
        self.config.read(self.path)
        return self.config.get(section, parametrName)
