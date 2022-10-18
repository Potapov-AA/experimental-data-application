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

        with open(self.path, "w") as configFiles:
            self.config .write(configFiles)

    def UpdateParametr(self, section, parametrName, value):
        self.config.set(section, parametrName, value)
        with open(self.path, "w") as configFiles:
            self.config.write(configFiles)

    def GetParametr(self, section, parametrName):
        self.config.read(self.path)
        return self.config.get(section, parametrName)
