# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
#                                                                              *
#  Jovem Programador                                                           *
#  Estudante de Engenharia de Telecomunicações                                 *
#  Tecnologia de Informação e de Medicina.                                     *
#  Foco Fé Força Paciência                                                     *
#  Allah no Comando.                                                           *
# ******************************************************************************
from os import makedirs, path
from random import randint
from sys import argv, exit
from time import sleep

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from gcrypter.db import G6RDB
from gcrypter.en import EN
from gcrypter.gfuns import debugpath, localpath, after
from gcrypter.pt import PT


class G6R:
    def __init__(self):
        self.gc = QApplication(argv)

        # application font
        QFontDatabase.addApplicationFont(f"{localpath()}/g6r-fonts/Abel.ttf")

        img = QPixmap(f"{localpath()}/g6r-icons/gcrypter-logo-01.png").scaled(QSize(500, 500))
        self.align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignAbsolute)
        self.color = Qt.GlobalColor.darkGreen

        self.janela = QSplashScreen(img)
        self.janela.setStyleSheet(theme)
        self.janela.show()
        self.iniciar()

    def iniciar(self):
        load = 0
        while load < 100:
            self.janela.showMessage(f"Loading ... {load}%", self.align, self.color)
            sleep(0.5)
            load += randint(1, 10)
        if path.exists(f"{debugpath()}/gcrypter.db"):
            config = G6RDB().return_data(_table='config')[0]
            if config[1] == 'English':
                app = EN()
                self.janela.close()
                app.ferramentas.show()
            elif config[1] == 'Portugues':
                app = PT()
                self.janela.close()
                app.ferramentas.show()
            else:
                perg = QMessageBox.question(self.janela, "X_X", "- Am sorry, the language set in your database is unsupported, Would you like to reconfigure it?\n\n"
                                                                "- Lamento, o idioma definido na sua base de dados não é suportada, Desejaria reconfigura-la?")
                if perg == QMessageBox.StandardButton.Yes:
                    G6RDB().update_config(_lang='English')
                    QMessageBox.information(self.janela, "^_^", "🤓👌🏽")
                return after(_sec=10, _do=exit(0))
        else:
            app = EN()
            self.janela.close()
            app.ferramentas.show()


if __name__ == '__main__':
    makedirs(debugpath(), exist_ok=True)
    G6RDB().update_config(_lang='English')
    G6RDB().insert_user()
    theme = open('g6r-themes/g6rlight.qss').read().strip()
    gcApp = G6R()
    gcApp.gc.exec()
