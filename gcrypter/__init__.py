# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
#                                                                              *
#  Jovem Programador                                                           *
#  Estudante de Engenharia de Telecomunicações                                 *
#  Tecnologia de Informação e de Medicina.                                     *
#  Foco Fé Força Paciência                                                     *
#  Allah no Comando.                                                           *
# ******************************************************************************
import os
from configparser import ConfigParser
from random import randint
from subprocess import getoutput
from sys import argv
from time import sleep

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from gcrypter.en import EN
from gcrypter.pt import PT


class G6R:
    def __init__(self):
        self.gc = QApplication(argv)

        # application font
        QFontDatabase.addApplicationFont("./fonts/Abel.ttf")

        img = QPixmap("icons/gcrypter-logo-02.png").scaled(QSize(500, 500))
        self.align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignAbsolute)
        self.color = Qt.GlobalColor.darkGreen

        self.janela = QSplashScreen(img)
        self.janela.setStyleSheet(theme)
        self.janela.show()
        self.iniciar()

    @property
    def debugpath(self) -> str:
        if os.name == 'posix':
            home = getoutput('echo $HOME')
            return os.path.join(home, '.gcr-debug')
        return '.gcr-debug'

    def iniciar(self):
        n = 0
        inifile = ConfigParser()
        load = 0
        while load < 100:
            self.janela.showMessage(f"Loading ... {load}%", self.align, self.color)
            sleep(0.5)
            load += randint(1, 10)
        if os.path.exists(f'{self.debugpath}/gcrypter.ini'):
            inifile.read(f'{self.debugpath}/gcrypter.ini')
            if inifile['MAIN']['lang'] == 'English':
                app = EN()
                app.ferramentas.show()
            elif inifile['MAIN']['lang'] == 'Portugues':
                app = PT()
                app.ferramentas.show()
            else:
                QMessageBox.critical(QWidget, 'Error', "- Am sorry, the language set in your [imagc.ini] file is unsupported!\n"
                                                       "- Lamento, o idioma definido no seu ficheiro [imagc.ini] não é suportado!")
        else:
            app = EN()
            app.ferramentas.show()


if __name__ == '__main__':
    theme = open('themes/gcrypter.qss').read().strip()
    gcApp = G6R()
    gcApp.gc.exec()
