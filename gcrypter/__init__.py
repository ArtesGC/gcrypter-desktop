# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
#                                                                              *
#  Jovem Programador                                                           *
#  Estudante de Engenharia de Telecomunicações                                 *
#  Tecnologia de Informação e de Medicina.                                     *
#  Foco Fé Força Paciência                                                     *
#  Allah no Comando.                                                           *
# ******************************************************************************
from os import path, name
from configparser import ConfigParser
from random import randint
from secrets import token_bytes
from subprocess import getoutput
from sys import argv
from time import sleep

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from gcrypter.en import EN
from gcrypter.pt import PT


def encrypt(p: str):
    """funcao encriptadora"""
    encriptar = p.encode()
    encriptar_ = token_bytes(len(p))

    encriptado = int.from_bytes(encriptar, 'big')
    encriptado_ = int.from_bytes(encriptar_, 'big')

    encriptado_final = encriptado ^ encriptado_
    return encriptado_final, encriptado_


def decrypt(p: int, q: int):
    """funcao desencriptadora"""
    palavra_encriptada = int(p) ^ int(q)
    desencriptada = palavra_encriptada.to_bytes((palavra_encriptada.bit_length() + 7) // 8, 'big')
    return desencriptada.decode()


def debugpath() -> str:
    if name == 'posix':
        home = getoutput('echo $HOME')
        return path.join(home, '.gcr-debug')
    return '.gcr-debug'


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
