# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
# ******************************************************************************
from configparser import ConfigParser
from datetime import datetime
from os import path, makedirs, listdir
from re import compile
from webbrowser import open_new

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from gcrypter.globalfunc import debugpath, encrypt, decrypt, perfilnome, created, logged, localpath

theme = open(f'{localpath()}/gcr-themes/gcrypter.qss').read().strip()


class EN:
    def __init__(self):
        self.ferramentas = QDialog()
        self.ferramentas.setFixedSize(QSize(700, 650))
        self.ferramentas.setWindowTitle('GCrypter')
        self.ferramentas.setWindowIcon(QIcon(f'{localpath()}/gcr-icons/favicon-192x192.png'))
        self.ferramentas.setStyleSheet(theme)

        # layout
        layout = QVBoxLayout()

        # menu-bar
        menu = QMenuBar()
        layout.setMenuBar(menu)
        detalhes = menu.addMenu('&Help')

        lang = detalhes.addAction('&Language')
        lang.triggered.connect(self._lang)

        instr = detalhes.addAction('&Instructions')
        instr.triggered.connect(self._instr)
        detalhes.addSeparator()

        sair = detalhes.addAction('&Quit')
        sair.triggered.connect(self._sair)

        sobre = menu.addAction('&About')
        sobre.triggered.connect(self._sobre)

        # tab-widget
        self.tab = QTabWidget(self.ferramentas)
        self.tab.setDocumentMode(True)
        self.tab.setTabBarAutoHide(True)
        layout.addWidget(self.tab)

        # copyright-label
        browser = lambda p: open_new('https://artesgc.home.blog')
        website = QLabel("<a href='#' style='text-decoration:none; color:white;'>™ ArtesGC, Inc.</a>")
        website.setAlignment(Qt.AlignmentFlag.AlignRight)
        website.setToolTip('Access to the official website of ArtesGC!')
        website.linkActivated.connect(browser)
        layout.addWidget(website)

        # global-variables
        self.utilizador = None
        self.moldura_editar = None
        self.moldura_principal = None
        self.moldura_codificar = None
        self.moldura_visualizar = None
        self.moldura_decodificar = None

        self.ferramentas.setLayout(layout)
        if len(listdir(debugpath())) > 1:
            self.usuarios_cadastrados()
        else:
            self.inicio_sessao()

    # getters and setters
    def perfilframe(self, _nome: str, _created: str, _lastlogin: str) -> QFrame:
        def inicio():
            pass

        def terminar():
            pass

        moldura = QFrame()
        layout1 = QFormLayout()
        layout2 = QHBoxLayout()

        layout1.addRow(QLabel(f"<h2>{_nome}</h2><hr>"))
        layout1.addRow("Created:", QLabel(f"<b>{_created}</b>"))
        layout1.addRow("Last Login:", QLabel(f"<b>{_lastlogin}</b>"))

        inicio_botao = QPushButton("Login")
        inicio_botao.setDefault(True)
        inicio_botao.clicked.connect(inicio)
        terminar_botao = QPushButton("Logout")
        terminar_botao.clicked.connect(terminar)
        layout2.addWidget(inicio_botao)
        layout2.addWidget(terminar_botao)
        layout1.addRow(layout2)

        moldura.setLayout(layout1)
        return moldura

    # menu-functions
    def _sair(self):
        resp = QMessageBox.question(self.ferramentas, 'Quit Program', 'Thank you for use our software.\n'
                                                                      'Please consider to visit our website and have a look to other options and services! - ArtesGC')
        if resp == QMessageBox.StandardButton.Yes:
            open_new('https://artesgc.home.blog')
        else:
            exit(0)

    def _sobre(self):
        QMessageBox.information(self.ferramentas, "About", """<ul>
<li>Name: GCrypter</li>
<li>Version: 0.9-112021</li>
<li>Designer & Programmer: Nurul-GC</li>
<li>Company: ArtesGC, Inc.</li>
</ul>""")

    def _instr(self):
        QMessageBox.information(self.ferramentas, "Instructions", """
Hello, Welcome to GCrypter<br>
It is a useful and practical tool for those<br>
who like to keep their files very well protected<br>
without having to worry about possible intrusions<br>
or even unwanted disclosures.<br>

<ul>
<li>GCrypter offers you options and a simple environment<br>
to you as an end user be able to register your thoughts<br>
and notes, saving them after ENCRYPTED..</li>
<li>There is also an option for DECRYPT the same files..</li>
<li>And even an option for EDIT files already encrypted.</li>
</ul>

Thank you very much for Support!<br>
Enjoy!<br><br>

© 2019-2021 Nurul-GC<br>
™ ArtesGC, Inc.""")

    def _lang(self):
        def alterar():
            try:
                config = ConfigParser()
                makedirs(debugpath(), exist_ok=True)
                if escolha_idioma.currentText() == 'Portugues':
                    config['MAIN'] = {'lang': escolha_idioma.currentText()}
                elif escolha_idioma.currentText() == 'English':
                    config['MAIN'] = {'lang': escolha_idioma.currentText()}
                with open(f'{debugpath()}/gcrypter.ini', 'w') as INIFILE:
                    config.write(INIFILE)
                QMessageBox.information(self.ferramentas, 'Successsful', 'The language set will be loaded after restart the program!')
                janela.close()
            except Exception as erro:
                QMessageBox.warning(self.ferramentas, 'Warning', f'While processing your request the following error was found:\n- {erro}')

        janela = QDialog(self.ferramentas)
        janela.setWindowTitle('Language')
        janela.setFixedSize(QSize(300, 200))
        layout = QVBoxLayout()

        labelInfo = QLabel('<h3>Choose the language:</h3>')
        layout.addWidget(labelInfo)

        idiomas = ['Portugues', 'English']
        escolha_idioma = QComboBox()
        escolha_idioma.addItems(idiomas)
        layout.addWidget(escolha_idioma)

        btnSalvar = QPushButton('Save')
        btnSalvar.clicked.connect(alterar)
        layout.addWidget(btnSalvar)

        janela.setLayout(layout)
        janela.show()

    # janelas
    def cadastro(self):
        janela_cadastro = QDialog(self.ferramentas)
        janela_cadastro.setWhatsThis('Registration: allows the user to personalize an account with a name and password!')
        janela_cadastro.setWindowTitle('Register')
        
        layout = QFormLayout()

        def guardar():
            if utilizador_cd.text() == '' or codigo.text() == '':
                QMessageBox.warning(self.ferramentas, 'Register', 'You Must Fill In Your Data Before Logging In..')
            else:
                if codigo.text() != codigo1.text():
                    QMessageBox.warning(self.ferramentas, 'Register', f'Am sorry {utilizador_cd.text()} the codes do not match..')
                else:
                    makedirs(f'{debugpath()}/G6r-{utilizador_cd.text()}', exist_ok=True)
                    with open(f'{debugpath()}/G6r-{utilizador_cd.text()}/user.log', 'w+') as file_user:
                        texto = f"""NAME: {utilizador_cd.text()}
PASSWORD: {codigo.text()}
ANSWER: {resposta.text()}"""
                        doc1, doc2 = encrypt(texto)
                        file_user.write(str(doc1) + '\n' + str(doc2))
                    created(_username=utilizador_cd.text())
                    janela_cadastro.destroy(True, True)
                    QMessageBox.information(self.ferramentas, 'Register',
                                            f"Congratulation {utilizador_cd.text()} your registration was successful\n"
                                            f"now log in to enjoy the program..")

        image = QLabel()
        image.setPixmap(QPixmap(f"{localpath()}/gcr-icons/01.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)

        utilizador_cd = QLineEdit()
        utilizador_cd.setToolTip('Required')
        utilizador_cd.setPlaceholderText('Type your Name..')
        layout.addRow(utilizador_cd)

        codigo = QLineEdit()
        codigo.setEchoMode(codigo.EchoMode.PasswordEchoOnEdit)
        codigo.setClearButtonEnabled(True)
        codigo.setToolTip('Required')
        codigo.setPlaceholderText('Type your Password..')
        layout.addRow(codigo)

        codigo1 = QLineEdit()
        codigo1.setEchoMode(codigo1.EchoMode.PasswordEchoOnEdit)
        codigo1.setClearButtonEnabled(True)
        codigo1.setToolTip('Required')
        codigo1.setPlaceholderText('Retype your Password..')
        codigo1.returnPressed.connect(guardar)
        layout.addRow(codigo1)

        resposta = QLineEdit()
        resposta.setToolTip('Required')
        resposta.setPlaceholderText('What is the most precious thing you have..')
        layout.addRow(resposta)

        guardar_botao = QPushButton('Login')
        guardar_botao.setDefault(True)
        guardar_botao.clicked.connect(guardar)
        layout.addRow(guardar_botao)

        janela_cadastro.setLayout(layout)
        janela_cadastro.show()

    def recuperar_senha(self):
        janela_recuperar_senha = QDialog(self.ferramentas)
        janela_recuperar_senha.setWhatsThis("About: User session recovery!\n"
                                            "You can always log in using this option if you permanently forget your password..")
        janela_recuperar_senha.setWindowTitle('Recover Password')

        layout = QFormLayout()

        image = QLabel()
        image.setPixmap(QPixmap(f"{localpath()}/gcr-icons/01.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)

        nome = QLineEdit()
        nome.setToolTip('Required')
        nome.setPlaceholderText('Type your Name..')
        layout.addRow(nome)

        resposta = QLineEdit()
        resposta.setToolTip('Required')
        resposta.setPlaceholderText('What is the most precious thing you have..')
        layout.addRow(resposta)

        def iniciar():
            try:
                with open(f'{debugpath()}/G6r-{nome.text()}/user.log', 'r+') as file_user:
                    file_ = file_user.readlines()
                    file = decrypt(int(file_[0]), int(file_[1]))
                    if nome.text() in file and resposta.text() in file:
                        logged(_username=nome.text())
                        janela_recuperar_senha.destroy(True, True)
                        self.tab.removeTab(self.tab.currentIndex())
                        return self._principal()
                    else:
                        question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                        f"Am sorry {nome.text()} your answer is wrong or you don't have an account yet..\n"
                                                        f"Register to keep using the program!")
                        if question == QMessageBox.StandardButton.Yes:
                            janela_recuperar_senha.destroy(True, True)
                            self.cadastro()
                        elif question == QMessageBox.StandardButton.No:
                            return exit(0)
            except FileNotFoundError:
                question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                f"Am sorry {nome.text()} You don't have an account yet..\n"
                                                f"Register to keep using the program!")
                if question == QMessageBox.StandardButton.Yes:
                    janela_recuperar_senha.destroy(True, True)
                    self.cadastro()
                elif question == QMessageBox.StandardButton.No:
                    return exit(0)

        confirmar = QPushButton('Confirm')
        confirmar.setDefault(True)
        confirmar.clicked.connect(iniciar)
        layout.addRow(confirmar)

        janela_recuperar_senha.setLayout(layout)
        janela_recuperar_senha.show()

    # molduras
    def usuarios_cadastrados(self):
        moldura_usuarios_cadastrados = QFrame()
        self.tab.addTab(moldura_usuarios_cadastrados, 'Registered Users')

        layout = QVBoxLayout()
        layout.addSpacing(10)

        for _dir in listdir(f"{debugpath()}/"):
            if path.isdir(_dir):
                nomeusuario = perfilnome(_dir)
                inifile = ConfigParser().read(f'{debugpath()}/G6r-{nomeusuario}/a5t_d5s.ini')
                criada = inifile['MAIN']['created']
                lastlogin = inifile['MAIN']['last_login']
                layout.addWidget(self.perfilframe(_nome=nomeusuario,
                                                  _created=criada,
                                                  _lastlogin=lastlogin))

        moldura_usuarios_cadastrados.setLayout(layout)

    def inicio_sessao(self):
        janela_inicio = QFrame()
        self.tab.addTab(janela_inicio, 'Home Session')

        layout = QFormLayout()

        image = QLabel()
        image.setPixmap(QPixmap(f"{localpath()}/gcr-icons/01.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)

        def iniciar():
            try:
                with open(f'{debugpath()}/G6r-{utilizador_is.text()}/user.log', 'r+') as file_user:
                    file_ = file_user.readlines()
                    file = decrypt(int(file_[0]), int(file_[1]))
                    if utilizador_is.text() in file and codigo.text() in file:
                        self.tab.removeTab(self.tab.currentIndex())
                        self.utilizador = utilizador_is.text()
                        logged(_username=self.utilizador)
                        return self._principal()
                    else:
                        question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                        f"Am sorry {utilizador_is.text()} You don't have an account yet..\n"
                                                        f"Register to keep using the program!")
                        if question == QMessageBox.StandardButton.Yes:
                            self.cadastro()
                        elif question == QMessageBox.StandardButton.No:
                            return exit(0)
            except FileNotFoundError:
                question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                f"Am sorry {utilizador_is.text()} You don't have an account yet..\n"
                                                f"Register to keep using the program!")
                if question == QMessageBox.StandardButton.Yes:
                    self.cadastro()
                elif question == QMessageBox.StandardButton.No:
                    return exit(0)

        utilizador_is = QLineEdit()
        utilizador_is.setToolTip('Required')
        utilizador_is.setPlaceholderText('Type Your Name..')
        layout.addRow(utilizador_is)

        codigo = QLineEdit()
        codigo.setEchoMode(codigo.EchoMode.PasswordEchoOnEdit)
        codigo.setClearButtonEnabled(True)
        codigo.setToolTip('Required')
        codigo.setPlaceholderText('Type Your Password..')
        codigo.returnPressed.connect(iniciar)
        layout.addRow(codigo)

        recuperar_senha = QLabel('<a href="#" style="text-decoration:none; color: white;">Forgot your password?</a>')
        recuperar_senha.setToolTip("Allows you to recover your login through your special answer provided in the registration\nIf you have not yet registered, do so now!")
        recuperar_senha.linkActivated.connect(self.recuperar_senha)
        recuperar_senha.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(recuperar_senha)

        iniciar_botao = QPushButton('Login')
        iniciar_botao.clicked.connect(iniciar)
        iniciar_botao.setDefault(True)
        layout.addRow(iniciar_botao)

        cadastro_botao = QPushButton('Register')
        cadastro_botao.clicked.connect(self.cadastro)
        layout.addRow(cadastro_botao)

        janela_inicio.setLayout(layout)

    def _principal(self):
        if self.moldura_principal is None:
            return self.principal()
        try:
            self.tab.setCurrentWidget(self.moldura_principal)
        except Exception:
            self.tab.removeTab(0)
            return self.principal()
        else:
            self.tab.removeTab(0)
            return self.principal()

    def principal(self):
        self.moldura_principal = QFrame()
        self.tab.addTab(self.moldura_principal, 'Welcome')
        self.tab.setCurrentWidget(self.moldura_principal)

        layout = QFormLayout()

        intro = QLabel('<h3><i>"Even if nothing is right, make sure everything goes well..<br>'
                       'GOD OFFERED YOU ANOTHER DAY, ENJOY IT!"</i></h3>')
        intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(intro)

        image = QLabel()
        image.setPixmap(QPixmap(f'{localpath()}/gcr-icons/02.jpg'))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)

        rotulo = QLabel('<h2>Select the Operation to Perform</h2>')
        rotulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(rotulo)

        vis_botao = QPushButton('Preview Encryption')
        vis_botao.clicked.connect(self._visualizar)
        layout.addRow(vis_botao)

        cod_botao = QPushButton('Encode')
        cod_botao.clicked.connect(self._codificar)
        layout.addRow(cod_botao)

        dec_botao = QPushButton('Decode')
        dec_botao.clicked.connect(self._decodificar)
        layout.addRow(dec_botao)

        editar_botao = QPushButton('Edit')
        editar_botao.clicked.connect(self._editar)
        layout.addRow(editar_botao)

        self.moldura_principal.setLayout(layout)

    def _codificar(self):
        if self.moldura_codificar is None:
            return self.codificar()
        try:
            self.tab.setCurrentWidget(self.moldura_codificar)
        except Exception:
            self.tab.removeTab(1)
            return self.codificar()
        else:
            self.tab.removeTab(1)
            return self.codificar()

    def codificar(self):
        def pe():
            if preview.isChecked():
                texto_enc.setHidden(False)
            else:
                texto_enc.setHidden(True)

        def guardar():
            if titulo.text() == '' or titulo.text().isspace():
                QMessageBox.critical(self.ferramentas, 'Fail', f"Am sorry {self.utilizador}, "
                                                               "please name the document before saving it!")
            else:
                makedirs(f'{debugpath()}/G6r-{self.utilizador}/docs', exist_ok=True)
                with open(f'{debugpath()}/G6r-{self.utilizador}/docs/{titulo.text()}.gc', 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(f"{doc1}\n{doc2}")
                QMessageBox.information(self.ferramentas, 'Alright', 'Successful Encrypted..')
                self.tab.removeTab(self.tab.currentIndex())
                self._principal()

        def textEdited():
            if texto.toPlainText().isascii():
                a, b = encrypt(texto.toPlainText())
                texto_enc.setText(f"{a}\n{b}")
            else:
                texto_enc.clear()

        self.moldura_codificar = QFrame()
        self.tab.addTab(self.moldura_codificar, 'New File')
        self.tab.setCurrentWidget(self.moldura_codificar)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        headlayout = QFormLayout()
        titulo = QLineEdit()
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setToolTip('Required')
        titulo.setPlaceholderText('Enter a name for the File..')

        preview = QRadioButton('Preview Encryption')
        preview.clicked.connect(pe)

        headlayout.addRow(preview, titulo)
        layout.addLayout(headlayout)

        texto = QTextEdit()
        texto.setFont(QFont('Abel', 10))
        texto.setAcceptRichText(True)
        texto.setAcceptDrops(True)
        texto.textChanged.connect(textEdited)
        texto.setPlaceholderText(f'What are you thinking {self.utilizador}..')
        layout.addWidget(texto)

        texto_enc = QTextEdit()
        texto_enc.setReadOnly(True)
        texto_enc.setHidden(True)
        texto_enc.setAcceptDrops(True)
        texto_enc.setPlaceholderText(f'Your encrypted text will be displayed here..')
        layout.addWidget(texto_enc)

        footlayout = QHBoxLayout()
        guardar_botao = QPushButton('Save')
        guardar_botao.setToolTip('Encrypted')
        guardar_botao.clicked.connect(guardar)
        guardar_botao.setDefault(True)
        footlayout.addWidget(guardar_botao)

        cancelar = lambda p: self.tab.removeTab(self.tab.currentIndex())
        cancelar_botao = QPushButton('Cancel')
        cancelar_botao.clicked.connect(cancelar)
        footlayout.addWidget(cancelar_botao)
        layout.addLayout(footlayout)

        self.moldura_codificar.setLayout(layout)

    def _decodificar(self):
        if self.moldura_decodificar is None:
            return self.decodificar()
        try:
            self.tab.setCurrentWidget(self.moldura_decodificar)
        except Exception:
            self.tab.removeTab(1)
            return self.decodificar()
        else:
            self.tab.removeTab(1)
            return self.decodificar()

    def decodificar(self):
        nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'{debugpath()}/G6r-{self.utilizador}/docs', filter='Files (*.gc)', caption='Select the file')
        try:
            with open(nome_file_open[0], 'r+') as file_decod:
                file_ = file_decod.readlines()
                file = decrypt(file_[0], file_[1])

            self.moldura_decodificar = QFrame()
            self.tab.addTab(self.moldura_decodificar, 'Reading File')
            self.tab.setCurrentWidget(self.moldura_decodificar)

            layout = QVBoxLayout()
            layout.setSpacing(10)

            texto = QTextEdit()
            texto.setReadOnly(True)
            texto.setFont(QFont('Abel', 10))
            texto.insertPlainText(file)
            layout.addWidget(texto)

            def fechar():
                with open(nome_file_open[0], 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(str(doc1) + '\n' + str(doc2))
                self.tab.removeTab(self.tab.currentIndex())

            fechar_botao = QPushButton('Close')
            fechar_botao.setDefault(True)
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            self.moldura_decodificar.setLayout(layout)
        except FileNotFoundError:
            QMessageBox.warning(self.ferramentas, 'Warning', 'File Not Found or Process Canceled!')

    def _editar(self):
        if self.moldura_editar is None:
            return self.editar()
        try:
            self.tab.setCurrentWidget(self.moldura_editar)
        except Exception:
            self.tab.removeTab(1)
            return self.editar()
        else:
            self.tab.removeTab(1)
            return self.editar()

    def editar(self):
        nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'{debugpath()}/G6r-{self.utilizador}/docs', filter='Files (*.gc)', caption='Select the file')
        try:
            with open(nome_file_open[0], 'r+') as file_decod:
                file_ = file_decod.readlines()
                file = decrypt(file_[0], file_[1])

            self.moldura_editar = QFrame()
            self.tab.addTab(self.moldura_editar, 'Editing File')
            self.tab.setCurrentWidget(self.moldura_editar)

            layout = QVBoxLayout()
            layout.setSpacing(10)

            texto = QTextEdit()
            texto.setFont(QFont('Abel', 10))
            texto.insertPlainText(file)
            layout.addWidget(texto)

            def guardar():
                with open(nome_file_open[0], 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(str(doc1) + '\n' + str(doc2))
                QMessageBox.information(self.ferramentas, 'Alright', 'Successful Encrypted 👌...')
                self.tab.removeTab(self.tab.currentIndex())
                self._principal()

            guardar_botao = QPushButton('Save')
            guardar_botao.setToolTip('Reencrypted')
            guardar_botao.clicked.connect(guardar)
            layout.addWidget(guardar_botao)

            def fechar():
                with open(nome_file_open[0], 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(str(doc1) + '\n' + str(doc2))
                self.tab.removeTab(self.tab.currentIndex())

            fechar_botao = QPushButton('Close')
            fechar_botao.setDefault(True)
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            self.moldura_editar.setLayout(layout)
        except FileNotFoundError:
            QMessageBox.warning(self.ferramentas, 'Warning', 'File Not Found or Process Canceled!')

    def _visualizar(self):
        if self.moldura_visualizar is None:
            return self.visualizar()
        try:
            self.tab.setCurrentWidget(self.moldura_visualizar)
        except Exception:
            self.tab.removeTab(1)
            return self.visualizar()
        else:
            self.tab.removeTab(1)
            return self.visualizar()

    def visualizar(self):
        self.moldura_visualizar = QFrame()
        self.tab.addTab(self.moldura_visualizar, 'Pre-viewing Encryption')
        self.tab.setCurrentWidget(self.moldura_visualizar)

        layout = QFormLayout()
        layout.setSpacing(10)
        layoutText = QHBoxLayout()

        def textEdited():
            if ptext.toPlainText().isascii():
                if ptext.toPlainText().split('\n')[0].isnumeric():
                    try:
                        ab = ptext.toPlainText().split('\n')
                        if len(ab) > 1:
                            rtext.setText(f"{decrypt(ab[0], ab[1])}")
                        else:
                            rtext.clear()
                    except Exception:
                        QMessageBox.critical(self.ferramentas, 'Encryption Error', 'Check if the values entered are correct..')
                        rtext.clear()
                else:
                    a, b = encrypt(ptext.toPlainText())
                    rtext.setText(f"{a}\n{b}")

        ptext = QTextEdit()
        ptext.setPlaceholderText(f"Type something {self.utilizador}..")
        ptext.textChanged.connect(textEdited)
        layoutText.addWidget(ptext)

        rtext = QTextEdit()
        rtext.setPlaceholderText("And the result will be transcribed to here..")
        rtext.setReadOnly(True)
        layoutText.addWidget(rtext)
        layout.addRow(layoutText)

        infoLabel = QLabel("""
<small>
<ul>
<li>This feature allows you to test and understand how GCrypter works.</li>
<li>You are also allowed to copy and paste values from one box to another.</li>
<li>Please feel free to try encrypting and decrypting anything you want to.</li>
</ul>
</small>""")
        layout.addRow(infoLabel)

        fechar = lambda: self.tab.removeTab(self.tab.currentIndex())
        fechar_botao = QPushButton('Close')
        fechar_botao.setDefault(True)
        fechar_botao.clicked.connect(fechar)
        layout.addRow(fechar_botao)

        self.moldura_visualizar.setLayout(layout)
