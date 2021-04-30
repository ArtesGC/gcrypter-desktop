#  Copyright (c) 2019-2020 Nurul GC
#  Direitos Autorais (c) 2019-2020 Nurul GC
#
#  Jovem Programador
#  Estudante de Engenharia de Telecomunicaçoes
#  Tecnologia de Informação e de Medicina.
#  Foco Fé Força Paciência
#  Allah no Comando.

from datetime import datetime
import os
import platform
import webbrowser
from sys import argv

import re
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from secrets import token_bytes


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
        self.ferramentas.setWindowTitle(f'GCrypter - Editando - {self.ficheiroExterno}')
        self.ferramentas.setWindowIcon(QIcon(f'{os.path.abspath(os.curdir)}/img/artesgc-512x512.png'))
        self.ferramentas.setPalette(QPalette(QColor('Wheat')))
        self.caixa_mensagem = QMessageBox()

        # secção do menu
        menu = QMenuBar(self.ferramentas)
        detalhes = menu.addMenu('&Ajuda')
        sobre = menu.addAction('&Sobre')
        sobre.triggered.connect(self.hello)
        instr = detalhes.addAction('&Instruções')
        instr.setIcon(QIcon(f'{os.path.abspath(os.curdir)}/img/info.bmp'))
        instr.triggered.connect(self.instr)
        detalhes.addSeparator()

        sair_ = lambda: self.gc.instance().quit()
        sair = detalhes.addAction('&Sair')
        sair.setIcon(QIcon(f'{os.path.abspath(os.curdir)}/img/nao2.bmp'))
        sair.triggered.connect(sair_)

        # verificação e validação do tipo de ficheiro
        if len(argv) >= 2:
            if argv[1].endswith('.gc'):
                self.ficheiroExterno = argv[1]
                self.editar()
            else:
                self.caixa_mensagem.critical(self.ferramentas, 'Erro', 'Arquivo inválido!')

    def hello(self):
        janela_hello = QDialog(self.ferramentas)
        janela_hello.setPalette(QPalette(QColor('Wheat')))
        janela_hello.setWhatsThis('Sobre: Apresentação dos Dados de Identificação do Programa!')
        janela_hello.setWindowTitle('Sobre')
        janela_hello.setFixedSize(400, 350)

        layout = QVBoxLayout()

        rotulo_qr = QLabel("<h2>Informações sobre Programa</h2>")
        rotulo_qr.setPixmap(QPixmap(f'{os.path.abspath(os.curdir)}/img/ArtesGC.png'))
        rotulo_qr.setAlignment(Qt.AlignCenter)
        rotulo_qr.setToolTip('Leia o Código QR\nCom Ajuda do Leitor de QR do seu Telemóvel!')
        layout.addWidget(rotulo_qr)

        rotulo_hello = QLabel("""<br>
Nome: <b>GCrypter</b><br>
Versão: <b>0.6.022021</b><br>
Designer & Programador: <b>Nurul GC</b><br>
Empresa: <b>ArtesGC, Inc.</b>
""")
        layout.addWidget(rotulo_hello)

        sair = lambda: janela_hello.close()
        sair_botao = QPushButton('Ok')
        sair_botao.clicked.connect(sair)
        layout.addWidget(sair_botao)

        janela_hello.setLayout(layout)
        janela_hello.show()

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

Direitos Autorais © 2019-2021 Nurul GC
Marca Registrada ArtesGC, Inc.
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
            texto.setFont(QFont('cambria', 10))
            texto.insertPlainText(file)
            layout.addWidget(texto)

            def guardar():
                with open(self.ficheiroExterno, 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(str(doc1) + '\n' + str(doc2))

                QMessageBox.information(self.ferramentas, 'Concluido', 'Codificação bem-sucedida..\n 🤝 👌')
                self.tab.removeTab(1)
                self.main0()

            guardar_botao = QPushButton('Salvar (Recodificado)')
            guardar_botao.clicked.connect(guardar)
            layout.addWidget(guardar_botao)

            fechar = lambda: self.gc.exit(0)
            fechar_botao = QPushButton('Sair')
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            janela_editar.setLayout(layout)
        except Exception as e:
            self.caixa_mensagem.warning(self.ferramentas, 'Erro', f'{e}')


class C9R:
    class PT:
        def __init__(self):
            self.gc = QApplication(argv)
            self.ferramentas = QWidget()
            self.ferramentas.setFixedSize(500, 400)
            self.ferramentas.setWindowTitle('GCrypter')
            self.ferramentas.setWindowIcon(QIcon(f'{os.path.abspath(os.curdir)}/img/artesgc-512x512.png'))
            self.ferramentas.setPalette(QPalette(QColor('Wheat')))

            menu = QMenuBar(self.ferramentas)
            detalhes = menu.addMenu('&Ajuda')
            sobre = menu.addAction('&Sobre')
            sobre.triggered.connect(self.hello)

            instr = detalhes.addAction('&Instruções')
            instr.setIcon(QIcon(f'{os.path.abspath(os.curdir)}/img/info.bmp'))
            instr.triggered.connect(self.instr)
            detalhes.addSeparator()

            sair_ = lambda: self.gc.exit(0)
            sair = detalhes.addAction('&Sair')
            sair.setIcon(QIcon(f'{os.path.abspath(os.curdir)}/img/nao2.bmp'))
            sair.triggered.connect(sair_)

            self.tab = QTabWidget(self.ferramentas)
            self.tab.setGeometry(0, 25, 500, 380)

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
Versão: 0.7.042021
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
            # janelaInicio.setPalette(QPalette(QColor('Wheat')))
            layout = QFormLayout()
            layout.setSpacing(15)

            image = QLabel()
            image.setPixmap(QPixmap(f"{os.path.abspath(os.curdir)}/img/alhamdulillah2.jpg"))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            def iniciar():
                try:
                    with open(f'G6r-{self.utilizador_is.text()}/utilizador.log', 'r+') as file_user:
                        file_ = file_user.readlines()
                        file = decrypt(int(file_[0]), int(file_[1]))
                        if self.utilizador_is.text() in file and codigo.text() in file:
                            self.tab.removeTab(0)
                            return self.main0()
                        else:
                            question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                            f'Lamento {self.utilizador_is.text()} Você Ainda Não Tem Uma Conta Criada..\nRegistre-se Para Ter Acesso ao Serviço!')
                            if question == 16384:
                                self.cadastro()
                            elif question == 65536:
                                return self.gc.exit(0)
                except FileNotFoundError:
                    question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                    f'Lamento {self.utilizador_is.text()} Você Ainda Não Tem Uma Conta Criada..\nRegistre-se Para Ter Acesso ao Serviço!')
                    if question == 16384:
                        self.cadastro()
                    elif question == 65536:
                        return self.gc.exit(0)

            self.utilizador_is = QLineEdit()
            self.utilizador_is.setToolTip('Obrigatório')
            layout.addRow('<b>Digite Seu &Nome: *</b>', self.utilizador_is)

            codigo = QLineEdit()
            codigo.setEchoMode(codigo.PasswordEchoOnEdit)
            codigo.setClearButtonEnabled(True)
            codigo.setToolTip('Obrigatório')
            codigo.returnPressed.connect(iniciar)
            layout.addRow('<b>Digite Sua &Senha: *</b>', codigo)

            recuperarSenha = QLabel('<a href="#" style="text-decoration:none;">Esqueceu sua senha?</a>')
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
            janelaCadastro.setPalette(QPalette(QColor('Wheat')))
            janelaCadastro.setWhatsThis('Cadastro: permite ao usuario personalizar uma conta com nome e senha!')
            janelaCadastro.setWindowTitle('Cadastro')
            janelaCadastro.setFixedSize(500, 250)
            layout = QFormLayout()
            layout.setSpacing(5)

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
    RESPOSTA: {resposta.text()}
    DATA-CRIACAO: {datetime.date(datetime.today())}"""
                                doc1, doc2 = encrypt(texto)
                                file_user.write(str(doc1) + '\n' + str(doc2))
                            janelaCadastro.destroy()
                            QMessageBox.information(self.ferramentas, 'Cadastro',
                                                    f'Parabens {self.utilizador_cd.text()} o seu cadastro foi bem sucedido\nagora inicie sessão para disfrutar do programa..')
                        else:
                            with open(f'G6r-{self.utilizador_cd.text()}/utilizador.log', 'w+') as file_user:
                                texto = f"""
    ********************
    * NOVO UTILIZADOR! *
    ********************
    
    NOME: {self.utilizador_cd.text()}
    SENHA: {codigo.text()}
    RESPOSTA: {resposta.text()}
    DATA-CRIACAO: {datetime.date(datetime.today())}"""
                                doc1, doc2 = encrypt(texto)
                                file_user.write(str(doc1) + '\n' + str(doc2))
                            janelaCadastro.destroy()
                            QMessageBox.information(self.ferramentas, 'Cadastro',
                                                    f'Parabens {self.utilizador_cd.text()} o seu cadastro foi bem sucedido\nagora inicie sessão para disfrutar do programa..')

            image = QLabel("<h3><i>Deus sabe, Deus ouve, Deus vê..</i></h3>")
            image.setPixmap(QPixmap(f'{os.path.abspath(os.curdir)}/img/Deus.jpg'))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            self.utilizador_cd = QLineEdit()
            self.utilizador_cd.setToolTip('Obrigatório')
            layout.addRow('<b>Digite Seu &Nome: *</b>', self.utilizador_cd)

            codigo = QLineEdit()
            codigo.setEchoMode(codigo.PasswordEchoOnEdit)
            codigo.setClearButtonEnabled(True)
            codigo.setToolTip('Obrigatório')
            layout.addRow('<b>Digite Sua &Senha: *</b>', codigo)

            codigo1 = QLineEdit()
            codigo1.setEchoMode(codigo1.PasswordEchoOnEdit)
            codigo1.setClearButtonEnabled(True)
            codigo1.setToolTip('Obrigatório')
            codigo1.returnPressed.connect(guardar)
            layout.addRow('<b>Redigite Sua &Senha: *</b>', codigo1)

            resposta = QLineEdit()
            resposta.setToolTip('Obrigatório')
            layout.addRow('<b>Qual é a coisa mais preciosa que você possui?</b>', resposta)

            guardar_botao = QPushButton('Entrar')
            guardar_botao.setDefault(True)
            guardar_botao.clicked.connect(guardar)
            layout.addRow(guardar_botao)
            janelaCadastro.setLayout(layout)
            janelaCadastro.show()

        def recuperarSenha(self):
            janela_recuperarSenha = QDialog(self.ferramentas)
            janela_recuperarSenha.setPalette(QPalette(QColor('Wheat')))
            janela_recuperarSenha.setWhatsThis('Sobre: Recuperação da sessão do úsuario!\nPoderá sempre iniciar sessão atravez desta opção caso esqueça permanentemente a sua senha..')
            janela_recuperarSenha.setWindowTitle('Recuperar Senha')
            janela_recuperarSenha.setFixedSize(500, 250)

            layout = QFormLayout()

            image = QLabel("<h3><i>Deus sabe, Deus ouve, Deus vê..</i></h3>")
            image.setPixmap(QPixmap(f'{os.path.abspath(os.curdir)}/img/Deus.jpg'))
            image.setAlignment(Qt.AlignCenter)
            layout.addRow(image)

            nome = QLineEdit()
            nome.setToolTip('Obrigatório')
            layout.addRow('<b>Digite o seu Nome: *</b>', nome)

            resposta = QLineEdit()
            resposta.setToolTip('Obrigatório')
            layout.addRow('<b>Qual é a coisa mais preciosa que você possui?</b>', resposta)

            def iniciar():
                try:
                    with open(f'G6r-{nome.text()}/utilizador.log', 'r+') as file_user:
                        file_ = file_user.readlines()
                        file = decrypt(int(file_[0]), int(file_[1]))
                        if nome.text() in file and resposta.text() in file:
                            janela_recuperarSenha.destroy(True, True)
                            self.tab.removeTab(0)
                            return self.main0()
                        else:
                            question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                            f'Lamento {nome.text()} a sua Resposta está Errada ou Você Ainda Não Tem Uma Conta Criada..\nRegistre-se Para Ter Acesso ao Serviço!')
                            if question == 16384:
                                janela_recuperarSenha.destroy(True, True)
                                self.cadastro()
                            elif question == 65536:
                                return self.gc.exit(0)
                except FileNotFoundError:
                    question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                    f'Lamento {nome.text()} Você Ainda Não Tem Uma Conta Criada..\nRegistre-se Para Ter Acesso ao Serviço!')
                    if question == 16384:
                        janela_recuperarSenha.destroy(True, True)
                        self.cadastro()
                    elif question == 65536:
                        return self.gc.instance().quit()

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
                self.tab.removeTab(0)
                return self.main_c9r()
            else:
                self.tab.removeTab(0)
                return self.main_c9r()

        def main_c9r(self):
            self.moldura_main = QFrame()
            self.moldura_main.setPalette(QPalette(QColor('Wheat')))
            self.tab.addTab(self.moldura_main, 'Bem-Vindo')
            self.tab.setCurrentWidget(self.moldura_main)

            layout = QFormLayout()
            layout.setSpacing(15)

            image = QLabel('<h3><i>"Mesmo que nada esteje bem, certifica te que tudo corra bem..\nDEUS TE OFERECEU MAIS UM DIA APROVEITE AO MAXIMO!"</i></h3>')
            image.setPixmap(QPixmap(f'{os.path.abspath(os.curdir)}/img/004.png'))
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
            rotulo2 = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC, Inc.</a>")
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
                self.tab.removeTab(1)
                return self.codificar()
            else:
                self.tab.removeTab(1)
                return self.codificar()

        def codificar(self):
            self.moldura_cod = QFrame()
            self.moldura_cod.setPalette(QPalette(QColor('Wheat')))
            self.tab.addTab(self.moldura_cod, 'Novo Arquivo')
            self.tab.setCurrentWidget(self.moldura_cod)

            layout = QVBoxLayout()

            hl = QFormLayout()
            titulo = QLineEdit()
            titulo.setAlignment(Qt.AlignCenter)
            titulo.setToolTip('Obrigatório')
            hl.addRow('<b>Digite um &Nome para o Arquivo: *</b>', titulo)
            layout.addLayout(hl)

            texto = QTextEdit()
            texto.setFont(QFont('cambria', 10))
            texto.setAcceptRichText(True)
            texto.setAcceptDrops(True)
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
                    self.tab.removeTab(1)
                    self.main0()

            hl = QHBoxLayout()
            guardar_botao = QPushButton('Guardar (Codificado)')
            guardar_botao.clicked.connect(guardar)
            guardar_botao.setDefault(True)
            hl.addWidget(guardar_botao)

            cancelar = lambda p: self.tab.removeTab(1)
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
                self.tab.removeTab(1)
                return self.decodificar()
            else:
                self.tab.removeTab(1)
                return self.decodificar()

        def decodificar(self):
            nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'G6r-{self.utilizador_is.text()}', filter='Ficheiros (*.gc)')
            try:
                with open(nome_file_open[0], 'r+') as file_decod:
                    file_ = file_decod.readlines()
                    file = decrypt(file_[0], file_[1])

                self.moldura_decod = QFrame()
                self.moldura_decod.setPalette(QPalette(QColor('Wheat')))
                self.tab.addTab(self.moldura_decod, 'Lendo Arquivo')
                self.tab.setCurrentWidget(self.moldura_decod)
                layout = QVBoxLayout()

                texto = QTextEdit(self.moldura_decod)
                texto.setReadOnly(True)
                texto.setFont(QFont('cambria', 10))
                texto.insertPlainText(file)
                layout.addWidget(texto)

                fechar = lambda: self.tab.removeTab(1)
                fechar_botao = QPushButton('Fechar')
                fechar_botao.clicked.connect(fechar)
                layout.addWidget(fechar_botao)
                self.moldura_decod.setLayout(layout)
            except FileNotFoundError:
                QMessageBox.warning(self.ferramentas, 'Aviso', 'Ficheiro Não Encontrado ou Processo Cancelado!')

        def editar(self):
            self.utilizador = (self.utilizador_is.text() or self.utilizador_cd.text())
            nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'G6r-{self.utilizador}', filter='Ficheiros (*.gc)')
            try:
                with open(nome_file_open[0], 'r+') as file_decod:
                    file_ = file_decod.readlines()
                    file = decrypt(file_[0], file_[1])

                self.moldura_editar = QFrame()
                self.moldura_editar.setPalette(QPalette(QColor('Wheat')))
                self.tab.addTab(self.moldura_editar, 'Editando Arquivo')
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

                    QMessageBox.information(self.ferramentas, 'Concluido', 'Codificação Bem Sucedida..\n 🤝 👌')
                    self.tab.removeTab(1)
                    self.main0()

                guardar_botao = QPushButton('Guardar (Recodificado)')
                guardar_botao.clicked.connect(guardar)
                layout.addWidget(guardar_botao)

                fechar = lambda: self.tab.removeTab(1)
                fechar_botao = QPushButton('Fechar')
                fechar_botao.clicked.connect(fechar)
                layout.addWidget(fechar_botao)
                self.moldura_editar.setLayout(layout)
            except FileNotFoundError:
                QMessageBox.warning(self.ferramentas, 'Aviso', 'Ficheiro Não Encontrado ou Processo Cancelado!')


if __name__ == '__main__':
    if len(argv) == 1:
        os.chdir(os.path.abspath(os.curdir))
        app = C9R()
        app.ferramentas.show()
        app.gc.exec_()
    elif len(argv) >= 2:
        os.chdir(os.path.abspath(os.curdir))
        app = EditarFicheiroExterno()
        app.ferramentas.show()
        app.gc.exec_()
    elif not os.path.exists(f"{os.path.abspath(os.curdir)}/img"):
        QMessageBox.critical(QMessageBox(), "Erro de inicialização", "Algum directorio obrigatório em falta.."
                                                                     "\nReinstale o programa ou reextraia os arquivos originais novamente para solucionar o problema"
                                                                     "\n(não se preocupe que os seus dados não serão perdidos)!")
