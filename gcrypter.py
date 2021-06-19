#  Copyright (c) 2019-2020 Nurul GC
#  Direitos Autorais (c) 2019-2020 Nurul GC
#
#  Jovem Programador
#  Estudante de Engenharia de Telecomunicações
#  Tecnologia de Informação e de Medicina.
#  Foco Fé Força Paciência
#  Allah no Comando.

import os
import re
import webbrowser
from datetime import datetime
from secrets import token_bytes
from sys import argv, exit
from time import sleep

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

appTheme = open('themes/gc-manjaromix.qss').read().strip()


def verificarData(frase: str):
    """funcao para extrair a data de um texto
    {datetime.today(datetime.date())}
    """
    data = ""
    dataRegex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    confirma = dataRegex.search(frase)
    if confirma:
        data = confirma.group()
    return data


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


class EditarFicheiroExterno:
    def __init__(self):
        self.ficheiroExterno = None

        self.gc = QApplication(argv)
        self.ferramentas = QWidget()
        self.ferramentas.setFixedSize(500, 400)
        self.ferramentas.setWindowTitle(f'GCrypter - Edit - {self.ficheiroExterno}')
        self.ferramentas.setWindowIcon(QIcon(f'img/gcrypter-icon.png'))
        self.ferramentas.setStyleSheet(appTheme)
        self.caixa_mensagem = QMessageBox()

        # secção do menu
        menu = QMenuBar(self.ferramentas)
        detalhes = menu.addMenu('&Help')
        sobre = menu.addAction('&About')
        sobre.triggered.connect(self.hello)
        instr = detalhes.addAction('&Instructions')
        instr.setIcon(QIcon(f'img/info.bmp'))
        instr.triggered.connect(self.instr)
        detalhes.addSeparator()

        sair_ = lambda: self.gc.instance().quit()
        sair = detalhes.addAction('&Quit')
        sair.setIcon(QIcon(f'img/nao2.bmp'))
        sair.triggered.connect(sair_)

        # verificação e validação do tipo de ficheiro
        if len(argv) >= 2:
            if argv[1].endswith('.gc'):
                self.ficheiroExterno = argv[1]
                self.editar()
            else:
                self.caixa_mensagem.critical(self.ferramentas, 'Error', 'Invalid file!')

    def hello(self):
        QMessageBox.information(self.ferramentas, "About", """
Name: GCrypter
Version: 0.7.042021
Designer & Programmer: Nurul GC
Company: ArtesGC, Inc.
""")

    def instr(self):
        QMessageBox.information(self.ferramentas, 'Instructions', """
Hello Welcome to GCrypter
It is a useful and practical tool for those
who like to keep their files very well protected
without having to worry about possible intrusions
or even unwanted disclosures.

- GCrypter offers you options and a simple environment
to you as an end user can register your thoughts,
data and notes, saving them later ENCODED..
- There is also the option of DECODING the same files..
- And even the option of EDITING files already encrypted.

Thank you very much for Support!
Enjoy!

© 2019-2021 Nurul GC
™ ArtesGC, Inc.
""")

    def editar(self):
        try:
            with open(self.ficheiroExterno, 'r+') as file_decod:
                file_ = file_decod.readlines()
                file = decrypt(file_[0], file_[1])

            janela_editar = QWidget(self.ferramentas)
            janela_editar.move(0, 25)
            layout = QVBoxLayout()

            texto = QTextEdit()
            texto.setFont(QFont('cambria', 12))
            texto.insertPlainText(file)
            layout.addWidget(texto)

            def guardar():
                with open(self.ficheiroExterno, 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(str(doc1) + '\n' + str(doc2))

                QMessageBox.information(self.ferramentas, 'Conclude', 'Successful encoding..\n 🤝 👌')
                self.tab.removeTab(self.tab.currentIndex())
                self.main0()

            guardar_botao = QPushButton('Save')
            guardar_botao.clicked.connect(guardar)
            layout.addWidget(guardar_botao)

            fechar = lambda: exit(0)
            fechar_botao = QPushButton('Quit')
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            janela_editar.setLayout(layout)
        except Exception as e:
            self.caixa_mensagem.warning(self.ferramentas, 'Error', f'{e}')


class G6R:
    def __init__(self):
        self.janela = QWidget()
        self.janela.setWindowTitle("GCrypter")
        self.janela.setWindowIcon(QIcon("img/gcrypter-icon.png"))
        self.janela.setStyleSheet(appTheme)

        layout = QVBoxLayout()

        labelImage = QLabel()
        labelImage.setPixmap(QPixmap("img/gcrypter.png").scaled(QSize(450, 450)))
        layout.addWidget(labelImage)

        listaIdiomas = ['Set language - Defina o idioma', 'English', 'Português']
        self.idiomas = QComboBox()
        self.idiomas.addItems(listaIdiomas)
        layout.addWidget(self.idiomas)

        self.barraIniciar = QProgressBar()
        self.barraIniciar.setOrientation(Qt.Horizontal)
        layout.addWidget(self.barraIniciar)

        botaoIniciar = QPushButton('In..')
        botaoIniciar.clicked.connect(self.iniciar)
        layout.addWidget(botaoIniciar)

        self.janela.setLayout(layout)

    def iniciar(self):
        n = 0
        if self.idiomas.currentText() == 'English':
            while n < 101:
                self.barraIniciar.setValue(n)
                sleep(0.5)
                n += 5
            self.janela.destroy()
            app = G6R.EN()
            app.ferramentas.show()
        elif self.idiomas.currentText() == 'Português':
            while n < 101:
                self.barraIniciar.setValue(n)
                sleep(0.3)
                n += 2
            self.janela.destroy()
            app = G6R.PT()
            app.ferramentas.show()
        else:
            QMessageBox.information(self.janela, "Info", "- Please select a language!\n- Por favor selecione um idioma!")

    class PT:
        def __init__(self):
            self.ferramentas = QWidget()
            self.ferramentas.setFixedSize(600, 600)
            self.ferramentas.setWindowTitle('GCrypter')
            self.ferramentas.setWindowIcon(QIcon('img/gcrypter-icon.png'))
            self.ferramentas.setStyleSheet(appTheme)

            menu = QMenuBar(self.ferramentas)
            detalhes = menu.addMenu('&Ajuda')
            sobre = menu.addAction('&Sobre')
            sobre.triggered.connect(self.hello)

            instr = detalhes.addAction('&Instruções')
            instr.triggered.connect(self.instr)
            detalhes.addSeparator()

            sair_ = lambda: exit(0)
            sair = detalhes.addAction('&Sair')
            sair.triggered.connect(sair_)

            self.tab = QTabWidget(self.ferramentas)
            self.tab.setGeometry(0, 25, 600, 580)

            self.moldura_main = None
            self.moldura_editar = None
            self.moldura_cod = None
            self.moldura_decod = None
            self.utilizador = None
            self.utilizador_is = None
            self.utilizador_cd = None

            self.inicio_sessao()

        def hello(self):
            QMessageBox.information(self.ferramentas, "Sobre", """
Nome: GCrypter
Versão: 0.8.072021
Designer & Programador: Nurul GC
Empresa: ArtesGC, Inc.
""")

        def instr(self):
            QMessageBox.information(self.ferramentas, 'Instruções', """
Olá Bem-Vindo ao GCrypter
Ele é uma ferramenta útil e prática para quem gosta de manter os seus arquivos
muito bem protegidos sem ter que se preocupar
com possíveis invasões ou até divulgações indesejadas..

- O GCrypter lhe oferece opções e um ambiente simples
para que você como utilizador final possa registrar os seus pensamentos,
dados e anotações, guardando-os posteriormente CODIFICADOS..
- Nele também está a opção de DECODIFICAÇÂO dos mesmos arquivos..
- E até a opção de EDIÇÂO dos arquivos já codificados..

Muito Obrigado Pelo Apoio!
Faça Bom Proveito!

© 2019-2021 Nurul GC
™ ArtesGC, Inc.
""")

        def inicio_sessao(self):
            janelaInicio = QWidget()
            self.tab.addTab(janelaInicio, 'Inicio Sessão')
            layout = QFormLayout()
            layout.setSpacing(15)

            image = QLabel()
            image.setPixmap(QPixmap("img/03.png"))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            def iniciar():
                try:
                    with open(f'G6r-{self.utilizador_is.text()}/utilizador.log', 'r+') as file_user:
                        file_ = file_user.readlines()
                        file = decrypt(int(file_[0]), int(file_[1]))
                        if self.utilizador_is.text() in file and codigo.text() in file:
                            self.tab.removeTab(self.tab.currentIndex())
                            return self.main0()
                        else:
                            question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                            f'Lamento {self.utilizador_is.text()} Você Ainda Não Tem Uma Conta Criada..\n'
                                                            f'Registre-se Para Ter Acesso ao Serviço!')
                            if question == QMessageBox.Yes:
                                self.cadastro()
                            elif question == QMessageBox.No:
                                return exit(0)
                except FileNotFoundError:
                    question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                    f'Lamento {self.utilizador_is.text()} Você Ainda Não Tem Uma Conta Criada..\n'
                                                    f'Registre-se Para Ter Acesso ao Serviço!')
                    if question == QMessageBox.Yes:
                        self.cadastro()
                    elif question == QMessageBox.No:
                        return exit(0)

            self.utilizador_is = QLineEdit()
            self.utilizador_is.setToolTip('Obrigatório')
            self.utilizador_is.setPlaceholderText('Digite o Seu Nome..')
            layout.addRow(self.utilizador_is)

            codigo = QLineEdit()
            codigo.setEchoMode(codigo.PasswordEchoOnEdit)
            codigo.setClearButtonEnabled(True)
            codigo.setToolTip('Obrigatório')
            codigo.returnPressed.connect(iniciar)
            codigo.setPlaceholderText('Digite a Sua Senha..')
            layout.addRow(codigo)

            recuperarSenha = QLabel('<a href="#" style="text-decoration:none; color: white;">Esqueceu a sua senha?</a>')
            recuperarSenha.setToolTip('Permite-lhe recuperar o seu login atravez da sua resposta especial fornecida no cadastro\nCaso ainda não tenha feito o cadastro, fá-lo já!')
            recuperarSenha.linkActivated.connect(self.recuperarSenha)
            recuperarSenha.setAlignment(Qt.AlignRight)
            layout.addWidget(recuperarSenha)

            iniciar_botao = QPushButton('Entrar')
            iniciar_botao.clicked.connect(iniciar)
            iniciar_botao.setDefault(True)
            layout.addRow(iniciar_botao)

            cadastro_botao = QPushButton('Cadastrar')
            cadastro_botao.clicked.connect(self.cadastro)
            layout.addRow(cadastro_botao)

            janelaInicio.setLayout(layout)

        def cadastro(self):
            janelaCadastro = QDialog(self.ferramentas)
            janelaCadastro.setWhatsThis('Cadastro: permite ao usuario personalizar uma conta com nome e senha!')
            janelaCadastro.setWindowTitle('Cadastro')
            janelaCadastro.setFixedSize(500, 500)
            layout = QFormLayout()
            layout.setSpacing(10)

            def guardar():
                if self.utilizador_cd.text() == '' and codigo.text() == '':
                    QMessageBox.warning(self.ferramentas, 'Cadastro', 'Você Deve Preencher os Seus Dados Antes de Entrar..')
                else:
                    if codigo.text() != codigo1.text():
                        QMessageBox.warning(self.ferramentas, 'Cadastro', f'Lamento {self.utilizador_cd.text()} os Códigos Não Correspondem..')
                    else:
                        if not os.path.exists(f'G6r-{self.utilizador_cd.text()}'):
                            os.mkdir(f'G6r-{self.utilizador_cd.text()}')
                        with open(f'G6r-{self.utilizador_cd.text()}/utilizador.log', 'w+') as file_user:
                            texto = f"""
********************
* NOVO UTILIZADOR! *
********************

NOME: {self.utilizador_cd.text()}
SENHA: {codigo.text()}
RESPOSTA: {resposta.text()}"""
                            doc1, doc2 = encrypt(texto)
                            file_user.write(str(doc1) + '\n' + str(doc2))
                        janelaCadastro.destroy()
                        QMessageBox.information(self.ferramentas, 'Cadastro',
                                                f"Parabens {self.utilizador_cd.text()} o seu cadastro foi bem sucedido\n"
                                                f"agora inicie sessão para disfrutar do programa..")

            image = QLabel()
            image.setPixmap(QPixmap("img/01.jpg"))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            self.utilizador_cd = QLineEdit()
            self.utilizador_cd.setToolTip('Obrigatório')
            self.utilizador_cd.setPlaceholderText('Digite o Seu Nome..')
            layout.addRow(self.utilizador_cd)

            codigo = QLineEdit()
            codigo.setEchoMode(codigo.PasswordEchoOnEdit)
            codigo.setClearButtonEnabled(True)
            codigo.setToolTip('Obrigatório')
            codigo.setPlaceholderText('Digite a Sua Senha..')
            layout.addRow(codigo)

            codigo1 = QLineEdit()
            codigo1.setEchoMode(codigo1.PasswordEchoOnEdit)
            codigo1.setClearButtonEnabled(True)
            codigo1.setToolTip('Obrigatório')
            codigo1.setPlaceholderText('Redigite a Sua Senha..')
            codigo1.returnPressed.connect(guardar)
            layout.addRow(codigo1)

            resposta = QLineEdit()
            resposta.setToolTip('Obrigatório')
            resposta.setPlaceholderText('Digite o nome da coisa mais preciosa que você possui..')
            layout.addRow(resposta)

            guardar_botao = QPushButton('Entrar')
            guardar_botao.setDefault(True)
            guardar_botao.clicked.connect(guardar)
            layout.addRow(guardar_botao)
            janelaCadastro.setLayout(layout)
            janelaCadastro.show()

        def recuperarSenha(self):
            janela_recuperarSenha = QDialog(self.ferramentas)
            janela_recuperarSenha.setWhatsThis("Sobre: Recuperação da sessão do úsuario!\n"
                                               "Poderá sempre iniciar sessão atravez desta opção caso esqueça permanentemente a sua senha..")
            janela_recuperarSenha.setWindowTitle('Recuperar Senha')
            janela_recuperarSenha.setFixedSize(500, 500)

            layout = QFormLayout()

            image = QLabel()
            image.setPixmap(QPixmap('img/01.jpg'))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            nome = QLineEdit()
            nome.setToolTip('Obrigatório')
            nome.setPlaceholderText('Digite o seu Nome..')
            layout.addRow(nome)

            resposta = QLineEdit()
            resposta.setToolTip('Obrigatório')
            resposta.setPlaceholderText('Digite o nome da coisa mais preciosa que você possui..')
            layout.addRow(resposta)

            def iniciar():
                try:
                    with open(f'G6r-{nome.text()}/utilizador.log', 'r+') as file_user:
                        file_ = file_user.readlines()
                        file = decrypt(int(file_[0]), int(file_[1]))
                        if nome.text() in file and resposta.text() in file:
                            janela_recuperarSenha.destroy(True, True)
                            self.tab.removeTab(self.tab.currentIndex())
                            return self.main0()
                        else:
                            question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                            f"Lamento {nome.text()} a sua Resposta está Errada ou Você Ainda Não Tem Uma Conta Criada..\n"
                                                            f"Registre-se Para Ter Acesso ao Serviço!")
                            if question == 16384:
                                janela_recuperarSenha.destroy(True, True)
                                self.cadastro()
                            elif question == 65536:
                                return exit(0)
                except FileNotFoundError:
                    question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                    f"Lamento {nome.text()} Você Ainda Não Tem Uma Conta Criada..\n"
                                                    f"Registre-se Para Ter Acesso ao Serviço!")
                    if question == 16384:
                        janela_recuperarSenha.destroy(True, True)
                        self.cadastro()
                    elif question == 65536:
                        return exit(0)

            confirmar = QPushButton('Confirmar')
            confirmar.setDefault(True)
            confirmar.clicked.connect(iniciar)
            layout.addRow(confirmar)
            janela_recuperarSenha.setLayout(layout)
            janela_recuperarSenha.show()

        def main0(self):
            if self.moldura_main is None:
                return self.main_c9r()
            try:
                self.tab.setCurrentWidget(self.moldura_main)
            except Exception as e:
                self.tab.removeTab(self.tab.currentIndex())
                return self.main_c9r()
            else:
                self.tab.removeTab(self.tab.currentIndex())
                return self.main_c9r()

        def main_c9r(self):
            self.moldura_main = QFrame()
            self.tab.addTab(self.moldura_main, 'Bem-Vindo')
            self.tab.setCurrentWidget(self.moldura_main)

            layout = QFormLayout()
            layout.setSpacing(15)

            image = QLabel('<h3><i>"Mesmo que nada esteje bem, certifica te que tudo corra bem..\nDEUS TE OFERECEU MAIS UM DIA APROVEITE AO MAXIMO!"</i></h3>')
            image.setPixmap(QPixmap('img/02.jpg'))
            image.setAlignment(Qt.AlignCenter)
            image.setToolTip('Mesmo que nada esteje bem, certifica te que tudo corra bem..\nDEUS TE OFERECEU MAIS UM DIA APROVEITE AO MAXIMO!')
            layout.addRow(image)

            rotulo = QLabel('<h2>Selecione a Operação a Executar</h2>')
            rotulo.setFont(QFont('cambria'))
            rotulo.setAlignment(Qt.AlignCenter)
            layout.addRow(rotulo)

            cod_botao = QPushButton('Codificar')
            cod_botao.clicked.connect(self.codificar1)
            layout.addRow(cod_botao)

            dec_botao = QPushButton('Decodificar')
            dec_botao.clicked.connect(self.decodificar2)
            layout.addRow(dec_botao)

            editar_botao = QPushButton('Editar')
            editar_botao.clicked.connect(self.editar)
            layout.addRow(editar_botao)

            browser = lambda p: webbrowser.open('https://artesgc.home.blog')
            rotulo2 = QLabel("<a href='#' style='text-decoration:none; color: white;'>ArtesGC, Inc.</a>")
            rotulo2.setAlignment(Qt.AlignRight)
            rotulo2.setToolTip('Acesso a pagina oficial da ArtesGC!')
            rotulo2.linkActivated.connect(browser)
            layout.addWidget(rotulo2)

            self.moldura_main.setLayout(layout)

        def codificar1(self):
            if self.moldura_cod is None:
                return self.codificar()
            try:
                self.tab.setCurrentWidget(self.moldura_cod)
            except Exception as e:
                self.tab.removeTab(self.tab.currentIndex())
                return self.codificar()
            else:
                self.tab.removeTab(self.tab.currentIndex())
                return self.codificar()

        def codificar(self):
            self.moldura_cod = QFrame()
            self.tab.addTab(self.moldura_cod, 'Novo Arquivo')
            self.tab.setCurrentWidget(self.moldura_cod)

            layout = QVBoxLayout()

            hl = QFormLayout()
            titulo = QLineEdit()
            titulo.setAlignment(Qt.AlignCenter)
            titulo.setToolTip('Obrigatório')
            titulo.setPlaceholderText('Digite um nome para o Arquivo..')
            hl.addRow(titulo)
            layout.addLayout(hl)

            texto = QTextEdit()
            texto.setFont(QFont('cambria', 12))
            texto.setAcceptRichText(True)
            texto.setAcceptDrops(True)
            texto.setPlaceholderText(f'Em que estas a pensar {self.utilizador_is.text()}..')
            layout.addWidget(texto)

            def guardar():
                if titulo.text() == '':
                    QMessageBox.critical(self.ferramentas, 'Codificar', f'Lamento {self.utilizador_is.text()}, por favor atribua um nome ao documento antes de guarda-lo!')
                else:
                    try:
                        with open(f'G6r-{self.utilizador_is.text()}/c8o-{titulo.text()}.gc', 'w+') as file_enc:
                            doc1, doc2 = encrypt(texto.toPlainText())
                            file_enc.write(str(doc1) + '\n' + str(doc2))
                    except FileNotFoundError:
                        os.mkdir(f'G6r-{self.utilizador_is.text()}')
                        with open(f'G6r-{self.utilizador_is.text()}/c8o-{titulo.text()}.gc', 'w+') as file_enc:
                            doc1, doc2 = encrypt(texto.toPlainText())
                            file_enc.write(f"{doc1}\n{doc2}")

                    QMessageBox.information(self.ferramentas, 'Concluido', 'Codificação Bem Sucedida..\n 🤝 👌')
                    self.tab.removeTab(self.tab.currentIndex())
                    self.main0()

            hl = QHBoxLayout()
            guardar_botao = QPushButton('Guardar')
            guardar_botao.setToolTip('Codificado')
            guardar_botao.clicked.connect(guardar)
            guardar_botao.setDefault(True)
            hl.addWidget(guardar_botao)

            cancelar = lambda p: self.tab.removeTab(self.tab.currentIndex())
            cancelar_botao = QPushButton('Cancelar')
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
                self.tab.removeTab(self.tab.currentIndex())
                return self.decodificar()
            else:
                self.tab.removeTab(self.tab.currentIndex())
                return self.decodificar()

        def decodificar(self):
            nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'G6r-{self.utilizador_is.text()}', filter='Ficheiros (*.gc)', caption='Selecione o arquivo')
            try:
                with open(nome_file_open[0], 'r+') as file_decod:
                    file_ = file_decod.readlines()
                    file = decrypt(file_[0], file_[1])

                self.moldura_decod = QFrame()
                self.tab.addTab(self.moldura_decod, 'Lendo Arquivo')
                self.tab.setCurrentWidget(self.moldura_decod)
                layout = QVBoxLayout()

                texto = QTextEdit(self.moldura_decod)
                texto.setReadOnly(True)
                texto.setFont(QFont('cambria', 12))
                texto.insertPlainText(file)
                layout.addWidget(texto)

                def fechar():
                    with open(nome_file_open[0], 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(str(doc1) + '\n' + str(doc2))
                    self.tab.removeTab(self.tab.currentIndex())

                fechar_botao = QPushButton('Fechar')
                fechar_botao.clicked.connect(fechar)
                layout.addWidget(fechar_botao)
                self.moldura_decod.setLayout(layout)
            except FileNotFoundError:
                QMessageBox.warning(self.ferramentas, 'Aviso', 'Ficheiro Não Encontrado ou Processo Cancelado!')

        def editar(self):
            self.utilizador = (self.utilizador_is.text() or self.utilizador_cd.text())
            nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'G6r-{self.utilizador}', filter='Ficheiros (*.gc)', caption='Selecione o arquivo')
            try:
                with open(nome_file_open[0], 'r+') as file_decod:
                    file_ = file_decod.readlines()
                    file = decrypt(file_[0], file_[1])

                self.moldura_editar = QFrame()
                self.tab.addTab(self.moldura_editar, 'Editando Arquivo')
                self.tab.setCurrentWidget(self.moldura_editar)
                layout = QVBoxLayout()

                texto = QTextEdit()
                texto.setFont(QFont('cambria', 12))
                texto.insertPlainText(file)
                layout.addWidget(texto)

                def guardar():
                    with open(nome_file_open[0], 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(str(doc1) + '\n' + str(doc2))

                    QMessageBox.information(self.ferramentas, 'Concluido', 'Codificação Bem Sucedida..\n 🤝 👌')
                    self.tab.removeTab(self.tab.currentIndex())
                    self.main0()

                guardar_botao = QPushButton('Guardar (Recodificado)')
                guardar_botao.clicked.connect(guardar)
                layout.addWidget(guardar_botao)

                def fechar():
                    with open(nome_file_open[0], 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(str(doc1) + '\n' + str(doc2))
                    self.tab.removeTab(self.tab.currentIndex())

                fechar_botao = QPushButton('Fechar')
                fechar_botao.clicked.connect(fechar)
                layout.addWidget(fechar_botao)
                self.moldura_editar.setLayout(layout)
            except FileNotFoundError:
                QMessageBox.warning(self.ferramentas, 'Aviso', 'Ficheiro Não Encontrado ou Processo Cancelado!')

    class EN:
        def __init__(self):
            self.ferramentas = QWidget()
            self.ferramentas.setFixedSize(600, 600)
            self.ferramentas.setWindowTitle('GCrypter')
            self.ferramentas.setWindowIcon(QIcon('img/gcrypter-icon.png'))
            self.ferramentas.setStyleSheet(appTheme)

            menu = QMenuBar(self.ferramentas)
            detalhes = menu.addMenu('&Help')
            sobre = menu.addAction('&About')
            sobre.triggered.connect(self.hello)

            instr = detalhes.addAction('&Instructions')
            instr.triggered.connect(self.instr)
            detalhes.addSeparator()

            sair_ = lambda: exit(0)
            sair = detalhes.addAction('&Quit')
            sair.triggered.connect(sair_)

            self.tab = QTabWidget(self.ferramentas)
            self.tab.setGeometry(0, 25, 600, 580)

            self.moldura_main = None
            self.moldura_editar = None
            self.moldura_cod = None
            self.moldura_decod = None
            self.utilizador = None
            self.utilizador_is = None
            self.utilizador_cd = None

            self.inicio_sessao()

        def hello(self):
            QMessageBox.information(self.ferramentas, "About", """
Name: GCrypter
Version: 0.8.072021
Designer & Programmer: Nurul GC
Company: ArtesGC, Inc.
""")

        def instr(self):
            QMessageBox.information(self.ferramentas, "Instructions", """
Hello Welcome to GCrypter
It is a useful and practical tool for those
who like to keep their files very well protected
without having to worry about possible intrusions
or even unwanted disclosures.

- GCrypter offers you options and a simple environment
to you as an end user can register your thoughts,
data and notes, saving them later ENCODED..
- There is also the option of DECODING the same files..
- And even the option of EDITING files already encrypted.

Thank you very much for Support!
Enjoy!

© 2019-2021 Nurul GC
™ ArtesGC, Inc.
""")

        def inicio_sessao(self):
            janelaInicio = QWidget()
            self.tab.addTab(janelaInicio, 'Home Session')
            layout = QFormLayout()
            layout.setSpacing(15)

            image = QLabel()
            image.setPixmap(QPixmap("img/03.png"))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            def iniciar():
                try:
                    with open(f'G6r-{self.utilizador_is.text()}/user.log', 'r+') as file_user:
                        file_ = file_user.readlines()
                        file = decrypt(int(file_[0]), int(file_[1]))
                        if self.utilizador_is.text() in file and codigo.text() in file:
                            self.tab.removeTab(self.tab.currentIndex())
                            return self.main0()
                        else:
                            question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                            f"Am sorry {self.utilizador_is.text()} You don't have an account yet..\n"
                                                            f"Register to Access the Service!")
                            if question == QMessageBox.Yes:
                                self.cadastro()
                            elif question == QMessageBox.No:
                                return exit(0)
                except FileNotFoundError:
                    question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                    f"Am sorry {self.utilizador_is.text()} You don't have an account yet..\n"
                                                    f"Register to Access the Service!")
                    if question == QMessageBox.Yes:
                        self.cadastro()
                    elif question == QMessageBox.No:
                        return exit(0)

            self.utilizador_is = QLineEdit()
            self.utilizador_is.setToolTip('Required')
            self.utilizador_is.setPlaceholderText('Type Your Name..')
            layout.addRow(self.utilizador_is)

            codigo = QLineEdit()
            codigo.setEchoMode(codigo.PasswordEchoOnEdit)
            codigo.setClearButtonEnabled(True)
            codigo.setToolTip('Required')
            codigo.setPlaceholderText('Type Your Password..')
            codigo.returnPressed.connect(iniciar)
            layout.addRow(codigo)

            recuperarSenha = QLabel('<a href="#" style="text-decoration:none; color: white;">Forgot your password?</a>')
            recuperarSenha.setToolTip("Allows you to recover your login through your special answer provided in the registration\nIf you have not yet registered, do so now!")
            recuperarSenha.linkActivated.connect(self.recuperarSenha)
            recuperarSenha.setAlignment(Qt.AlignRight)
            layout.addWidget(recuperarSenha)

            iniciar_botao = QPushButton('Enter')
            iniciar_botao.clicked.connect(iniciar)
            iniciar_botao.setDefault(True)
            layout.addRow(iniciar_botao)

            cadastro_botao = QPushButton('Register')
            cadastro_botao.clicked.connect(self.cadastro)
            layout.addRow(cadastro_botao)

            janelaInicio.setLayout(layout)

        def cadastro(self):
            janelaCadastro = QDialog(self.ferramentas)
            janelaCadastro.setWhatsThis('Registration: allows the user to personalize an account with a name and password!')
            janelaCadastro.setWindowTitle('Register')
            janelaCadastro.setFixedSize(QSize(500, 500))
            layout = QFormLayout()
            layout.setSpacing(10)

            def guardar():
                if self.utilizador_cd.text() == '' and codigo.text() == '':
                    QMessageBox.warning(self.ferramentas, 'Register', 'You Must Fill In Your Data Before Logging In..')
                else:
                    if codigo.text() != codigo1.text():
                        QMessageBox.warning(self.ferramentas, 'Register', f'Am sorry {self.utilizador_cd.text()} the codes do not match..')
                    else:
                        if not os.path.exists(f'G6r-{self.utilizador_cd.text()}'):
                            os.mkdir(f'G6r-{self.utilizador_cd.text()}')
                        with open(f'G6r-{self.utilizador_cd.text()}/user.log', 'w+') as file_user:
                            texto = f"""
*************
* NEW USER! *
*************

NAME: {self.utilizador_cd.text()}
PASSWORD: {codigo.text()}
ANSWER: {resposta.text()}"""
                            doc1, doc2 = encrypt(texto)
                            file_user.write(str(doc1) + '\n' + str(doc2))
                        janelaCadastro.destroy()
                        QMessageBox.information(self.ferramentas, 'Register',
                                                f"Congratulation {self.utilizador_cd.text()} your registration was successful\n"
                                                f"now log in to enjoy the program..")

            image = QLabel()
            image.setPixmap(QPixmap("img/01.jpg"))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            self.utilizador_cd = QLineEdit()
            self.utilizador_cd.setToolTip('Required')
            self.utilizador_cd.setPlaceholderText('Type your Name..')
            layout.addRow(self.utilizador_cd)

            codigo = QLineEdit()
            codigo.setEchoMode(codigo.PasswordEchoOnEdit)
            codigo.setClearButtonEnabled(True)
            codigo.setToolTip('Required')
            codigo.setPlaceholderText('Type your Password..')
            layout.addRow(codigo)

            codigo1 = QLineEdit()
            codigo1.setEchoMode(codigo1.PasswordEchoOnEdit)
            codigo1.setClearButtonEnabled(True)
            codigo1.setToolTip('Required')
            codigo1.setPlaceholderText('Retype your Password..')
            codigo1.returnPressed.connect(guardar)
            layout.addRow(codigo1)

            resposta = QLineEdit()
            resposta.setToolTip('Required')
            resposta.setPlaceholderText('Type the name of the most precious thing you have..')
            layout.addRow(resposta)

            guardar_botao = QPushButton('Enter')
            guardar_botao.setDefault(True)
            guardar_botao.clicked.connect(guardar)
            layout.addRow(guardar_botao)
            janelaCadastro.setLayout(layout)
            janelaCadastro.show()

        def recuperarSenha(self):
            janela_recuperarSenha = QDialog(self.ferramentas)
            janela_recuperarSenha.setWhatsThis("About: User session recovery!\n"
                                               "You can always log in using this option if you permanently forget your password..")
            janela_recuperarSenha.setWindowTitle('Recover Password')
            janela_recuperarSenha.setFixedSize(500, 500)

            layout = QFormLayout()

            image = QLabel()
            image.setPixmap(QPixmap('img/01.jpg'))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            nome = QLineEdit()
            nome.setToolTip('Required')
            nome.setPlaceholderText('Type your Name..')
            layout.addRow(nome)

            resposta = QLineEdit()
            resposta.setToolTip('Required')
            resposta.setPlaceholderText('Type the name of the most precious thing you have..')
            layout.addRow(resposta)

            def iniciar():
                try:
                    with open(f'G6r-{nome.text()}/user.log', 'r+') as file_user:
                        file_ = file_user.readlines()
                        file = decrypt(int(file_[0]), int(file_[1]))
                        if nome.text() in file and resposta.text() in file:
                            janela_recuperarSenha.destroy(True, True)
                            self.tab.removeTab(self.tab.currentIndex())
                            return self.main0()
                        else:
                            question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                            f"Am sorry {nome.text()} your answer is wrong or you don't have an account yet..\n"
                                                            f"Register to Access the Service!")
                            if question == 16384:
                                janela_recuperarSenha.destroy(True, True)
                                self.cadastro()
                            elif question == 65536:
                                return exit(0)
                except FileNotFoundError:
                    question = QMessageBox.question(self.ferramentas, 'Login Failed',
                                                    f"Am sorry {nome.text()} You don't have an account yet..\n"
                                                    f"Register to Access the Service!")
                    if question == 16384:
                        janela_recuperarSenha.destroy(True, True)
                        self.cadastro()
                    elif question == 65536:
                        return exit(0)

            confirmar = QPushButton('Confirm')
            confirmar.setDefault(True)
            confirmar.clicked.connect(iniciar)
            layout.addRow(confirmar)
            janela_recuperarSenha.setLayout(layout)
            janela_recuperarSenha.show()

        def main0(self):
            if self.moldura_main is None:
                return self.main_c9r()
            try:
                self.tab.setCurrentWidget(self.moldura_main)
            except Exception as e:
                self.tab.removeTab(self.tab.currentIndex())
                return self.main_c9r()
            else:
                self.tab.removeTab(self.tab.currentIndex())
                return self.main_c9r()

        def main_c9r(self):
            self.moldura_main = QFrame()
            self.tab.addTab(self.moldura_main, 'Welcome')
            self.tab.setCurrentWidget(self.moldura_main)

            layout = QFormLayout()
            layout.setSpacing(15)

            image = QLabel()
            image.setPixmap(QPixmap('img/02.jpg'))
            image.setAlignment(Qt.AlignCenter)
            image.setToolTip("Even if nothing is right, make sure everything goes well..\n"
                             "GOD OFFERED YOU ANOTHER DAY ENJOY IT!")
            layout.addRow(image)

            rotulo = QLabel('<h2>Select the Operation to Perform</h2>')
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

            browser = lambda p: webbrowser.open('https://artesgc.home.blog')
            rotulo2 = QLabel("<a href='#' style='text-decoration:none; color: white;'>™ ArtesGC, Inc.</a>")
            rotulo2.setAlignment(Qt.AlignRight)
            rotulo2.setToolTip('Access to the official website of ArtesGC!')
            rotulo2.linkActivated.connect(browser)
            layout.addWidget(rotulo2)

            self.moldura_main.setLayout(layout)

        def codificar1(self):
            if self.moldura_cod is None:
                return self.codificar()
            try:
                self.tab.setCurrentWidget(self.moldura_cod)
            except Exception as e:
                self.tab.removeTab(self.tab.currentIndex())
                return self.codificar()
            else:
                self.tab.removeTab(self.tab.currentIndex())
                return self.codificar()

        def codificar(self):
            self.moldura_cod = QFrame()
            self.tab.addTab(self.moldura_cod, 'New File')
            self.tab.setCurrentWidget(self.moldura_cod)

            layout = QVBoxLayout()

            hl = QFormLayout()
            titulo = QLineEdit()
            titulo.setAlignment(Qt.AlignCenter)
            titulo.setToolTip('Required')
            titulo.setPlaceholderText('Enter a name for the File..')
            hl.addRow(titulo)
            layout.addLayout(hl)

            texto = QTextEdit()
            texto.setFont(QFont('cambria', 12))
            texto.setAcceptRichText(True)
            texto.setAcceptDrops(True)
            texto.setPlaceholderText(f'What are you thinking {self.utilizador_is.text()}..')
            layout.addWidget(texto)

            def guardar():
                if titulo.text() == '' or titulo.text().isspace():
                    QMessageBox.critical(self.ferramentas, 'Encode', f"Am sorry {self.utilizador_is.text()}, please name the document before saving it!")
                else:
                    if not os.path.exists(f'G6r-{self.utilizador_is.text()}/thoughts'):
                        os.mkdir(f'G6r-{self.utilizador_is.text()}/thoughts')

                    with open(f'G6r-{self.utilizador_is.text()}/thoughts/{titulo.text()}.gc', 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(f"{doc1}\n{doc2}")

                    QMessageBox.information(self.ferramentas, 'Conclude', 'Successful Coding..')
                    self.tab.removeTab(self.tab.currentIndex())
                    self.main0()

            hl = QHBoxLayout()
            guardar_botao = QPushButton('Save')
            guardar_botao.setToolTip('Encoded')
            guardar_botao.clicked.connect(guardar)
            guardar_botao.setDefault(True)
            hl.addWidget(guardar_botao)

            cancelar = lambda p: self.tab.removeTab(self.tab.currentIndex())
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
                self.tab.removeTab(self.tab.currentIndex())
                return self.decodificar()
            else:
                self.tab.removeTab(1)
                return self.decodificar()

        def decodificar(self):
            nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'G6r-{self.utilizador_is.text()}/thoughts', filter='Files (*.gc)', caption='Select the file')
            try:
                with open(nome_file_open[0], 'r+') as file_decod:
                    file_ = file_decod.readlines()
                    file = decrypt(file_[0], file_[1])

                self.moldura_decod = QFrame()
                self.moldura_decod.setPalette(QPalette(QColor('wheat')))
                self.tab.addTab(self.moldura_decod, 'Reading File')
                self.tab.setCurrentWidget(self.moldura_decod)
                layout = QVBoxLayout()

                texto = QTextEdit(self.moldura_decod)
                texto.setReadOnly(True)
                texto.setFont(QFont('cambria', 12))
                texto.insertPlainText(file)
                layout.addWidget(texto)

                def fechar():
                    with open(nome_file_open[0], 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(str(doc1) + '\n' + str(doc2))
                    self.tab.removeTab(self.tab.currentIndex())

                fechar_botao = QPushButton('Close')
                fechar_botao.clicked.connect(fechar)
                layout.addWidget(fechar_botao)
                self.moldura_decod.setLayout(layout)
            except FileNotFoundError:
                QMessageBox.warning(self.ferramentas, 'Warning', 'File Not Found or Process Canceled!')

        def editar(self):
            self.utilizador = (self.utilizador_is.text() or self.utilizador_cd.text())
            nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'G6r-{self.utilizador}/thoughts', filter='Files (*.gc)', caption='Select the file')
            try:
                with open(nome_file_open[0], 'r+') as file_decod:
                    file_ = file_decod.readlines()
                    file = decrypt(file_[0], file_[1])

                self.moldura_editar = QFrame()
                self.moldura_editar.setPalette(QPalette(QColor('wheat')))
                self.tab.addTab(self.moldura_editar, 'Editing File')
                self.tab.setCurrentWidget(self.moldura_editar)
                layout = QVBoxLayout()

                texto = QTextEdit()
                texto.setFont(QFont('cambria', 12))
                texto.insertPlainText(file)
                layout.addWidget(texto)

                def guardar():
                    with open(nome_file_open[0], 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(str(doc1) + '\n' + str(doc2))

                    QMessageBox.information(self.ferramentas, 'Conclude', 'Successful Coding..\n 🤝 👌')
                    self.tab.removeTab(self.tab.currentIndex())
                    self.main0()

                guardar_botao = QPushButton('Save')
                guardar_botao.setToolTip('Rencoded')
                guardar_botao.clicked.connect(guardar)
                layout.addWidget(guardar_botao)

                def fechar():
                    with open(nome_file_open[0], 'w+') as file_enc:
                        doc1, doc2 = encrypt(texto.toPlainText())
                        file_enc.write(str(doc1) + '\n' + str(doc2))
                    self.tab.removeTab(self.tab.currentIndex())

                fechar_botao = QPushButton('Close')
                fechar_botao.clicked.connect(fechar)
                layout.addWidget(fechar_botao)
                self.moldura_editar.setLayout(layout)
            except FileNotFoundError:
                QMessageBox.warning(self.ferramentas, 'Warning', 'File Not Found or Process Canceled!')


if __name__ == '__main__':
    if len(argv) == 1:
        gc = QApplication(argv)
        gcApp = G6R()
        gcApp.janela.show()
        gc.exec_()
    elif len(argv) >= 2:
        gcApp = EditarFicheiroExterno()
        gcApp.ferramentas.show()
        gcApp.gc.exec_()
