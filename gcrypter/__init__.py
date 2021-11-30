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

        img = QPixmap(f"{localpath()}/g6r-icons/favicons/favicon-512x512.png")
        self.align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignAbsolute)
        self.color = Qt.GlobalColor.green

        self.janela = QSplashScreen(img)
        self.janela.setStyleSheet(theme)
        self.janela.show()
        self.iniciar()

    def iniciar(self):
        load = ''
        while len(load) < 100:
            self.janela.showMessage(f"[ {load} ]", self.align, self.color)
            sleep(0.5)
            load += "|"*randint(1, 10)

        if lang == 'English':
            app = EN()
            self.janela.close()
            app.ferramentas.setStyleSheet(theme)
            app.ferramentas.show()
        elif lang == 'Portugues':
            app = PT()
            self.janela.close()
            app.ferramentas.setStyleSheet(theme)
            app.ferramentas.show()
        else:
            perg = QMessageBox.question(self.janela, "X_X", "- Am sorry, the language set in your database is unsupported, Would you like to reconfigure it?\n\n"
                                                            "- Lamento, o idioma definido na sua base de dados não é suportada, Desejaria reconfigura-la?")
            if perg == QMessageBox.StandardButton.Yes:
                gdb.update_config(_lang='English')
                QMessageBox.information(self.janela, "^_^", "🤓👌🏽")
            return after(_sec=10, _do=exit(0))


if __name__ == '__main__':
    makedirs(debugpath(), exist_ok=True)

    gdb = G6RDB()
    if not path.exists(f"{debugpath()}/gcrypter.db"):
        gdb.update_config(_lang='English', _theme='Light')
        gdb.insert_user()

    lang = gdb.return_data(_table='config')[0][1]
    theme = gdb.return_data(_table='config')[0][2]
    if theme == 'Dark':
        theme = open(f"{localpath()}/g6r-themes/g6rdark.qss").read().strip()
    else:
        theme = open(f"{localpath()}/g6r-themes/g6rlight.qss").read().strip()

    gcApp = G6R()
    gcApp.gc.exec()
