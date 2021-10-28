# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
#                                                                              *
#  Jovem Programador                                                           *
#  Estudante de Engenharia de Telecomunicações                                 *
#  Tecnologia de Informação e de Medicina.                                     *
#  Foco Fé Força Paciência                                                     *
#  Allah no Comando.                                                           *
# ******************************************************************************
from configparser import ConfigParser
from os import path
from random import randint
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
        QFontDatabase.addApplicationFont("gcr-fonts/Abel.ttf")

        img = QPixmap("gcr-icons/gcrypter-logo-02.png").scaled(QSize(500, 500))
        self.align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignAbsolute)
        self.color = Qt.GlobalColor.darkGreen

        self.janela = QSplashScreen(img)
        self.janela.setStyleSheet(theme)
        self.janela.show()
        self.iniciar()

    def iniciar(self):
        n = 0
        inifile = ConfigParser()
        load = 0
        while load < 100:
            self.janela.showMessage(f"Loading ... {load}%", self.align, self.color)
            sleep(0.5)
            load += randint(1, 10)
        if path.exists(f'{debugpath()}/gcrypter.ini'):
            inifile.read(f'{debugpath()}/gcrypter.ini')
            if inifile['MAIN']['lang'] == 'English':
                app = EN()
                app.ferramentas.show()
            elif inifile['MAIN']['lang'] == 'Portugues':
                app = PT()
                app.ferramentas.show()
            else:
                QMessageBox.critical(QWidget, 'X_X', "- Am sorry, the language set in your [imagc.ini] file is unsupported!\n"
                                                     "- Lamento, o idioma definido no seu ficheiro [imagc.ini] não é suportado!")
        else:
            app = EN()
            app.ferramentas.show()


if __name__ == '__main__':
    theme = open('gcr-themes/gcrypter.qss').read().strip()
    gcApp = G6R()
    gcApp.gc.exec()
