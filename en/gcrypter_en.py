#  Copyright (c) 2019-2020 Nurul GC
#  Direitos Autorais (c) 2019-2020 Nurul GC
#
#  Jovem Programador
#  Estudante de Engenharia de Telecomunicaçoes
#  Tecnologia de Informação e de Medicina.
#  Foco Fé Força Paciência
#  Allah no Comando.

import os
import webbrowser
from sys import argv
from typing import List

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from secrets import token_bytes


def encrypt(p: str):
    """encoder function"""
    encriptar = p.encode()
    encriptar_ = token_bytes(len(p))

    encriptado = int.from_bytes(encriptar, 'big')
    encriptado_ = int.from_bytes(encriptar_, 'big')

    encriptado_final = encriptado ^ encriptado_
    return encriptado_final, encriptado_


def decrypt(p: int, q: int):
    """decoder function"""
    palavra_encriptada = int(p) ^ int(q)
    desencriptada = palavra_encriptada.to_bytes((palavra_encriptada.bit_length() + 7) // 8, 'big')
    return desencriptada.decode()


class EditarFicheiroExterno:
    def __init__(self):
        self.gc = QApplication(argv)
        self.ferramenta = QWidget()
        self.ferramenta.setWindowTitle(f'GCrypter - Editing - {self.ficheiroExterno}')
        self.ferramenta.setWindowIcon(QIcon('img/artesgc.ico'))
        self.caixa_mensagem = QMessageBox()

        # menu section
        menu = QMenuBar(self.ferramenta)
        detalhes = menu.addMenu('&Help')
        detalhes.setFont(QFont('tahoma', 8))
        detalhes.setPalette(QPalette(QColor('Wheat')))
        sobre = menu.addAction('&About')
        sobre.triggered.connect(self.hello)
        instr = detalhes.addAction('&Instruction')
        instr.setIcon(QIcon('img/info.bmp'))
        instr.triggered.connect(self.instr)
        detalhes.addSeparator()
        sair_ = lambda: self.gc.instance().quit()
        sair = detalhes.addAction('&Exit')
        sair.setIcon(QIcon('img/nao2.bmp'))
        sair.triggered.connect(sair_)

        # file type verification and validation
        if len(argv) >= 2:
            if argv[1].endswith('.gc'):
                self.ficheiroExterno = argv[1]
                self.editar()
            else:
                self.caixa_mensagem.critical(self.ferramenta, 'Error', 'Invalid file!')

    def editar(self):
        try:
            with open(self.ficheiroExterno, 'r+') as file_decod:
                file_ = file_decod.readlines()
                file = decrypt(file_[0], file_[1])

            layout = QVBoxLayout()

            texto = QTextEdit()
            texto.setFont(QFont('cambria', 10))
            texto.insertPlainText(file)
            layout.addWidget(texto)

            def guardar():
                with open(self.ficheiroExterno, 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(str(doc1) + '\n' + str(doc2))

                QMessageBox.information(self.ferramentas, 'Concluded', 'Successful Coding..\n 🤝 👌')
                self.tab.removeTab(1)
                self.main0()

            guardar_botao = QPushButton('Save (Recoded)')
            guardar_botao.clicked.connect(guardar)
            layout.addWidget(guardar_botao)

            fechar = lambda: self.gc.instance().quit()
            fechar_botao = QPushButton('Close')
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            self.ferramenta.setLayout(layout)
        except Exception as e:
            self.caixa_mensagem.warning(self.ferramenta, 'Error', f'{e}')


class C9R:
    def __init__(self):
        self.gc = QApplication(argv)
        self.ferramentas = QWidget()
        self.ferramentas.setFixedSize(400, 400)
        self.ferramentas.setWindowTitle('GCrypter')
        self.ferramentas.setWindowIcon(QIcon('img/artesgc.ico'))
        self.ferramentas.setPalette(QPalette(QColor('Wheat')))

        menu = QMenuBar(self.ferramentas)
        detalhes = menu.addMenu('&Help')
        detalhes.setFont(QFont('tahoma', 8))
        detalhes.setPalette(QPalette(QColor('Wheat')))
        sobre = menu.addAction('&About')
        # sobre.setText('&Sobre')
        sobre.triggered.connect(self.hello)
        
        instr = detalhes.addAction('&Instruction')
        instr.setIcon(QIcon('img/info.bmp'))
        instr.triggered.connect(self.instr)
        detalhes.addSeparator()
        sair_ = lambda: self.gc.instance().quit()
        sair = detalhes.addAction('&Exit')
        sair.setIcon(QIcon('img/nao2.bmp'))
        sair.triggered.connect(sair_)
        
        self.tab = QTabWidget(self.ferramentas)
        self.tab.setGeometry(0, 22, 400, 380)
        
        self.moldura_main = None
        self.moldura_cod = None
        self.moldura_decod = None
        self.utilizador = None

        self.inicio_sessao()

    def inicio_sessao(self):
        janelaInicio = QWidget()
        self.tab.addTab(janelaInicio, 'Home Session')
        # janelaInicio.setPalette(QPalette(QColor('Wheat')))
        layout = QFormLayout()
        layout.setSpacing(15)

        image = QLabel()
        image.setPixmap(QPixmap("img/alhamdulillah.jpg"))
        image.setAlignment(Qt.AlignCenter)
        layout.addRow(image)

        def iniciar():
            try:
                with open(f'E6E{self.utilizador_is.text()}/user.log', 'r+') as file_user:
                    file_ = file_user.readlines()
                    file = decrypt(int(file_[0]), int(file_[1]))
                    if self.utilizador_is.text() in file and codigo.text() in file:
                        self.tab.removeTab(0)
                        return self.main0()
                    else:
                        question = QMessageBox.question(self.ferramentas, "Login Failed", f"Am Sorry {self.utilizador_is.text()} You don't have any account created yet..\nSign-up to get full access!")
                        if question == 16384:
                            self.cadastro()
                        elif question == 65536:
                            return self.gc.instance().quit()
            except FileNotFoundError:
                question = QMessageBox.question(self.ferramentas, "Login Failed", f"Am Sorry {self.utilizador_is.text()} You don't have any account created yet..\nSign-up to get full access!")
                if question == 16384:
                    self.cadastro()
                elif question == 65536:
                    return self.gc.instance().quit()

        self.utilizador_is = QLineEdit()
        self.utilizador_is.setToolTip('Required')
        layout.addRow('Enter your &Name: *', self.utilizador_is)

        codigo = QLineEdit()
        codigo.setEchoMode(codigo.PasswordEchoOnEdit)
        codigo.setClearButtonEnabled(True)
        codigo.setToolTip('Required')
        codigo.returnPressed.connect(iniciar)
        layout.addRow('Enter your &Password: *', codigo)

        recuperarSenha = QLabel('<a href="#">Forgot your password?</a>')
        recuperarSenha.setToolTip('Allows you to recover your login through your special answer provided in the registration\nIf you have not yet registered, do so now!')
        recuperarSenha.linkActivated.connect(self.recuperarSenha)
        recuperarSenha.setAlignment(Qt.AlignRight)
        layout.addWidget(recuperarSenha)

        iniciar_botao = QPushButton('logIn')
        iniciar_botao.clicked.connect(iniciar)
        iniciar_botao.setDefault(True)
        layout.addRow(iniciar_botao)

        cadastro_botao = QPushButton('Register')
        cadastro_botao.clicked.connect(self.cadastro)
        layout.addRow(cadastro_botao)

        janelaInicio.setLayout(layout)

    def recuperarSenha(self):
        janela_recuperarSenha = QDialog(self.ferramentas)
        janela_recuperarSenha.setPalette(QPalette(QColor('Wheat')))
        janela_recuperarSenha.setWhatsThis('About: User session recovery!\nYou can always log in using this option if you permanently forget your password..')
        janela_recuperarSenha.setWindowTitle('Recover Password')
        janela_recuperarSenha.setFixedSize(400, 250)

        layout = QFormLayout()

        image = QLabel()
        image.setPixmap(QPixmap('img/God.jpg'))
        image.setAlignment(Qt.AlignCenter)
        layout.addRow(image)

        nome = QLineEdit()
        nome.setToolTip('Required')
        layout.addRow('Enter your &Name: *', nome)

        resposta = QLineEdit()
        resposta.setToolTip('Required')
        layout.addRow('What is the most precious thing you have?', resposta)

        def iniciar():
            try:
                with open(f'E6E{nome.text()}/user.log', 'r+') as file_user:
                    file_ = file_user.readlines()
                    file = decrypt(int(file_[0]), int(file_[1]))
                    if nome.text() in file and resposta.text() in file:
                        janela_recuperarSenha.destroy(True, True)
                        self.tab.removeTab(0)
                        return self.main0()
                    else:
                        question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                        f"Am Sorry {nome.text()} Your Answer is Wrong or You Don't Have an Account Created Yet.\nRegister to Access the Service!")
                        if question == 16384:
                            janela_recuperarSenha.destroy(True, True)
                            self.cadastro()
                        elif question == 65536:
                            return self.gc.instance().quit()
            except FileNotFoundError:
                question = QMessageBox.question(self.ferramentas, 'Login Failed', f"Am Sorry {nome.text()} You don't have an account yet.\nRegister to access the service!")
                if question == 16384:
                    janela_recuperarSenha.destroy(True, True)
                    self.cadastro()
                elif question == 65536:
                    return self.gc.instance().quit()

        confirmar = QPushButton('Confirm')
        confirmar.setDefault(True)
        confirmar.clicked.connect(iniciar)
        layout.addRow(confirmar)
        janela_recuperarSenha.setLayout(layout)
        janela_recuperarSenha.show()

    def cadastro(self):
        janelaCadastro = QDialog(self.ferramentas)
        janelaCadastro.setPalette(QPalette(QColor('Wheat')))
        janelaCadastro.setWhatsThis('Registration: allows the user to personalize an account with name and password!')
        janelaCadastro.setWindowTitle('Register')
        janelaCadastro.setFixedSize(400, 250)
        layout = QFormLayout()
        layout.setSpacing(5)

        def guardar():
            if self.utilizador_cd.text() == '' and codigo.text() == '':
                QMessageBox.warning(self.ferramentas, 'Register', 'You Must Fill In Your Data Before Logging In..')
            else:
                if codigo.text() != codigo1.text():
                    QMessageBox.warning(self.ferramentas, 'Register',
                                        f'Am sorry {self.utilizador_cd.text()} codes do not match..')
                else:
                    if not os.path.exists(f'C9R{self.utilizador_cd.text()}'):
                        os.mkdir(f'E6E{self.utilizador_cd.text()}')
                        with open(f'E6E{self.utilizador_cd.text()}/user.log', 'w+') as file_user:
                            texto = f"""
********************
*     NEW USER     *
********************

NAME: {self.utilizador_cd.text()}
PASSWORD: {codigo.text()}
ANSWER: {resposta.text()}"""
                            doc1, doc2 = encrypt(texto)
                            file_user.write(str(doc1) + '\n' + str(doc2))
                        janelaCadastro.destroy()
                        QMessageBox.information(self.ferramentas, 'Register',
                                                f'Congratulations {self.utilizador_cd.text()} your registration was successful\nnow log in to enjoy the program..')
                    else:
                        with open(f'E6E{self.utilizador_cd.text()}/user.log', 'w+') as file_user:
                            texto = f"""
********************
*     NEW USER     *
********************

NAME: {self.utilizador_cd.text()}
PASSWORD: {codigo.text()}
ANSWER: {resposta.text()}"""
                            doc1, doc2 = encrypt(texto)
                            file_user.write(str(doc1) + '\n' + str(doc2))
                        janelaCadastro.destroy()
                        QMessageBox.information(self.ferramentas, 'Register',
                                                f'Congratulations {self.utilizador_cd.text()} your registration was successful\nnow log in to enjoy the program..')

        image = QLabel()
        image.setPixmap(QPixmap('img/God.jpg'))
        image.setAlignment(Qt.AlignCenter)
        layout.addRow(image)

        self.utilizador_cd = QLineEdit()
        self.utilizador_cd.setToolTip('Required')
        layout.addRow('Enter your &Name: *', self.utilizador_cd)

        codigo = QLineEdit()
        codigo.setEchoMode(codigo.PasswordEchoOnEdit)
        codigo.setClearButtonEnabled(True)
        codigo.setToolTip('Required')
        layout.addRow('Enter your &Password: *', codigo)

        codigo1 = QLineEdit()
        codigo1.setEchoMode(codigo1.PasswordEchoOnEdit)
        codigo1.setClearButtonEnabled(True)
        codigo1.setToolTip('Required')
        codigo1.returnPressed.connect(guardar)
        layout.addRow('Retype your &Password: *', codigo1)

        resposta = QLineEdit()
        resposta.setToolTip('Required')
        layout.addRow('What is the most precious thing you have?', resposta)

        guardar_botao = QPushButton('logIn')
        guardar_botao.setDefault(True)
        guardar_botao.clicked.connect(guardar)
        layout.addRow(guardar_botao)
        janelaCadastro.setLayout(layout)
        janelaCadastro.show()
    
    def hello(self):
        janela_hello = QDialog(self.ferramentas)
        janela_hello.setPalette(QPalette(QColor('Wheat')))
        janela_hello.setWhatsThis('About: Presentation of Program Identification Data!')
        janela_hello.setWindowTitle('Sobre')
        janela_hello.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        
        rotulo_qr = QLabel()
        rotulo_qr.setPixmap(QPixmap('img/ArtesGC.png'))
        rotulo_qr.setAlignment(Qt.AlignCenter)
        rotulo_qr.setToolTip('Read the Code\nWith QRCode Reader on Your Phone!')
        layout.addWidget(rotulo_qr)
        
        rotulo_hello = QLabel("""Name: GCrypter
Version: 0.5-012021
Designer & Programmer: Nurul GC
Trademark: ArtesGC, Inc. - https://artesgc.home.blog
""")
        rotulo_hello.setAutoFillBackground(True)
        layout.addWidget(rotulo_hello)
        
        sair = lambda: janela_hello.close()
        sair_botao = QPushButton('Ok')
        sair_botao.clicked.connect(sair)
        layout.addWidget(sair_botao)
        
        janela_hello.setLayout(layout)
        janela_hello.exec()
    
    def instr(self):
        QMessageBox.information(self.ferramentas, 'Instruction', """
Hello Welcome To GCrypter
It is an Useful Tool For Who Like To Keep His Files
Very Well Saved Without Care About
Possible Invasions or Perhaps Undesirable Shares..

- GCrypter Offer Options and a Simple Environment
For You As End User Be Able To Save Your Thoughts, and Notes, ENCRYPTED..
- On it is also the Option to DECRYPT these Files..
- And to EDIT files already saved..

Thanks very much for your support!
Enjoy it!

Copyright © 2019-2021 Nurul GC
TradeMark ArtesGC, Inc.
""")
    
    def main0(self):
        if self.moldura_main is None:
            return self.main_c9r()
        try:
            self.tab.setCurrentWidget(self.moldura_main)
        except Exception as e:
            self.tab.removeTab(0)
            return self.main_c9r()
        else:
            self.tab.removeTab(0)
            return self.main_c9r()
    
    def main_c9r(self):
        self.moldura_main = QFrame()
        self.moldura_main.setPalette(QPalette(QColor('Wheat')))
        self.tab.addTab(self.moldura_main, 'Welcome')
        self.tab.setCurrentWidget(self.moldura_main)
        
        layout = QFormLayout()
        layout.setSpacing(10)
        
        image = QLabel()
        image.setPixmap(QPixmap('img/004.png'))
        image.setAlignment(Qt.AlignCenter)
        image.setToolTip('Even if nothing is right, make sure everything goes well.\nGOD HAS OFFERED YOU ONE MORE DAY ENJOY!')
        layout.addRow(image)
        
        rotulo = QLabel('Select the Operation to Perform')
        rotulo.setFont(QFont('cambria', 12))
        rotulo.setAlignment(Qt.AlignCenter)
        layout.addRow(rotulo)
        
        cod_botao = QPushButton('Encode')
        cod_botao.clicked.connect(self.codificar1)
        layout.addRow(cod_botao)
        
        dec_botao = QPushButton('Decode')
        dec_botao.clicked.connect(self.decodificar2)
        layout.addRow(dec_botao)
        
        editar_botao = QPushButton('Edit')
        editar_botao.clicked.connect(self.editar)
        layout.addRow(editar_botao)
        
        rotulo2 = QLabel("<a href='https://artesgc.home.blog'>ArtesGC, Inc.</a>")
        rotulo2.setAlignment(Qt.AlignRight)
        rotulo2.setToolTip("Access to ArtesGC's official website!")
        rotulo2.linkActivated.connect(self.hello)
        layout.addWidget(rotulo2)
        
        self.moldura_main.setLayout(layout)
    
    def codificar1(self):
        if self.moldura_cod is None:
            return self.codificar()
        try:
            self.tab.setCurrentWidget(self.moldura_cod)
        except Exception as e:
            self.tab.removeTab(1)
            return self.codificar()
        else:
            self.tab.removeTab(1)
            return self.codificar()
    
    def codificar(self):
        self.moldura_cod = QFrame()
        self.moldura_cod.setPalette(QPalette(QColor('Wheat')))
        self.tab.addTab(self.moldura_cod, 'New File')
        self.tab.setCurrentWidget(self.moldura_cod)
        
        layout = QVBoxLayout()
        
        hl = QFormLayout()
        titulo = QLineEdit()
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setToolTip('Required')
        hl.addRow('Enter a &Name for the File: *', titulo)
        layout.addLayout(hl)
        
        texto = QTextEdit()
        texto.setFont(QFont('cambria', 10))
        texto.setAcceptRichText(True)
        texto.setAcceptDrops(True)
        layout.addWidget(texto)
        
        def guardar():
            if titulo.text() == '':
                QMessageBox.critical(self.ferramentas, 'Codify',
                                     f'Am Sorry {self.utilizador_is.text()}, please name the document before saving it!')
            else:
                try:
                    with open(f'E6E{self.utilizador_is.text()}/e7d-{titulo.text()}.gc', 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(str(doc1) + '\n' + str(doc2))
                except FileNotFoundError:
                    os.mkdir(f'E6E{self.utilizador_is.text()}')
                    with open(f'E6E{self.utilizador_is.text()}/e7d-{titulo.text()}.gc', 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(f"{doc1}\n{doc2}")

                QMessageBox.information(self.ferramentas, 'Concluded', 'Successful Coding..\n 🤝 👌')
                self.tab.removeTab(1)
                self.main0()

        hl = QHBoxLayout()
        guardar_botao = QPushButton('Save (Coded)')
        guardar_botao.clicked.connect(guardar)
        guardar_botao.setDefault(True)
        hl.addWidget(guardar_botao)

        cancelar = lambda p: self.tab.removeTab(1)
        cancelar_botao = QPushButton('Cancel')
        cancelar_botao.clicked.connect(cancelar)
        cancelar_botao.setDefault(True)
        hl.addWidget(cancelar_botao)
        layout.addLayout(hl)
        self.moldura_cod.setLayout(layout)
    
    def decodificar2(self):
        if self.moldura_decod is None:
            return self.decodificar()
        try:
            self.tab.setCurrentWidget(self.moldura_decod)
        except Exception as e:
            self.tab.removeTab(1)
            return self.decodificar()
        else:
            self.tab.removeTab(1)
            return self.decodificar()
    
    def decodificar(self):
        nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'C9R{self.utilizador_is.text()}',
                                                     filter='Files (*.gc)')
        try:
            with open(nome_file_open[0], 'r+') as file_decod:
                file_ = file_decod.readlines()
                file = decrypt(file_[0], file_[1])
            
            self.moldura_decod = QFrame()
            self.moldura_decod.setPalette(QPalette(QColor('Wheat')))
            self.tab.addTab(self.moldura_decod, 'Reading File')
            self.tab.setCurrentWidget(self.moldura_decod)
            layout = QVBoxLayout()
            
            texto = QTextEdit(self.moldura_decod)
            texto.setReadOnly(True)
            texto.setFont(QFont('cambria', 10))
            texto.insertPlainText(file)
            layout.addWidget(texto)
            
            fechar = lambda: self.tab.removeTab(1)
            fechar_botao = QPushButton('Close')
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            self.moldura_decod.setLayout(layout)
        except FileNotFoundError:
            QMessageBox.warning(self.ferramentas, 'Warning', 'File Not Found or Process Canceled!')
    
    def editar(self):
        self.utilizador = (self.utilizador_is.text() or self.utilizador_cd.text())
        nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'E6E{self.utilizador}', filter='Files (*.gc)')
        try:
            with open(nome_file_open[0], 'r+') as file_decod:
                file_ = file_decod.readlines()
                file = decrypt(file_[0], file_[1])
            
            self.moldura_editar = QFrame()
            self.moldura_editar.setPalette(QPalette(QColor('Wheat')))
            self.tab.addTab(self.moldura_editar, 'Editing File')
            self.tab.setCurrentWidget(self.moldura_editar)
            layout = QVBoxLayout()
            
            texto = QTextEdit()
            texto.setFont(QFont('cambria', 10))
            texto.insertPlainText(file)
            layout.addWidget(texto)
            
            def guardar():
                with open(nome_file_open[0], 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(str(doc1) + '\n' + str(doc2))

                QMessageBox.information(self.ferramentas, 'Concluded', 'Successful Coding..\n 🤝 👌')
                self.tab.removeTab(1)
                self.main0()
            
            guardar_botao = QPushButton('Save (Recoded)')
            guardar_botao.clicked.connect(guardar)
            layout.addWidget(guardar_botao)
            
            fechar = lambda: self.tab.removeTab(1)
            fechar_botao = QPushButton('Close')
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            self.moldura_editar.setLayout(layout)
        except FileNotFoundError:
            QMessageBox.warning(self.ferramentas, 'Warning', 'File Not Found or Process Canceled!')


if __name__ == '__main__':
    if len(argv) == 1:
        app = C9R()
        app.ferramentas.show()
        app.gc.exec_()
    elif len(argv) >= 2:
        app = EditarFicheiroExterno()
        app.ferramenta.show()
        app.gc.exec_()
