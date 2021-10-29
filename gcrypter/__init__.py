# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
#                                                                              *
#  Jovem Programador                                                           *
#  Estudante de Engenharia de Telecomunicações                                 *
#  Tecnologia de Informação e de Medicina.                                     *
#  Foco Fé Força Paciência                                                     *
#  Allah no Comando.                                                           *
# ******************************************************************************
from os import makedirs
from random import randint
from sys import argv, exit
from time import sleep

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from gcrypter.db import G6RDB
from gcrypter.en import EN
from gcrypter.globalfunc import debugpath, localpath, after
from gcrypter.pt import PT


class G6R:
    def __init__(self):
        self.gc = QApplication(argv)

        # application font
        QFontDatabase.addApplicationFont(f"{localpath()}/gcr-fonts/Abel.ttf")

        img = QPixmap(f"{localpath()}/gcr-icons/gcrypter-logo-01.png").scaled(QSize(500, 500))
        self.align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignAbsolute)
        self.color = Qt.GlobalColor.green

        self.janela = QSplashScreen(img)
        self.janela.setStyleSheet(theme)
        self.janela.show()
        self.iniciar()

    def iniciar(self):
        n = 0
        config = G6RDB().return_data(_table='config')[0]
        load = 0
        while load < 100:
            self.janela.showMessage(f"Loading ... {load}%", self.align, self.color)
            sleep(0.5)
            load += randint(1, 10)
        if config[1] == 'English':
            app = EN()
            app.ferramentas.show()
        elif config[1] == 'Portugues':
            app = PT()
            app.ferramentas.show()
        else:
            perg = QMessageBox.question(self.janela, "X_X", "- Am sorry, the language set in your database is unsupported, Would you like to reconfigure it?\n\n"
                                                            "- Lamento, o idioma definido no sua base de dados não é suportada, Desejaria reconfigura-la?")
            if perg == QMessageBox.StandardButton.Yes:
                G6RDB().update_config(_lang='English')
                QMessageBox.information(self.janela, "^_^", "")
            return after(_sec=10, _do=exit(0))


if __name__ == '__main__':
    makedirs(debugpath(), exist_ok=True)
    theme = open('gcr-themes/gcrypter.qss').read().strip()
    gcApp = G6R()
    gcApp.gc.exec()
