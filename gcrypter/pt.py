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

from gcrypter import debugpath, encrypt, decrypt

theme = open('gcr-themes/gcrypter.qss').read().strip()


def perfilnome(_folder: str) -> str or None:
    nome = compile("G6r-[aA-zZ]+")
    if nome.match(_folder):
        return _folder.split("-")[-1]
    return None


def created(_username: str):
    config = ConfigParser()
    config['MAIN'] = {'created': datetime.today()}
    with open(f"{debugpath()}/G6r-{_username}/a5t_d5s.ini", "w+") as inifile:
        config.write(inifile)


def logged(_username: str):
    config = ConfigParser()
    config['MAIN'] = {'last_login': datetime.today()}
    with open(f"{debugpath()}/G6r-{_username}/a5t_d5s.ini", "w+") as inifile:
        config.write(inifile)


class PT:
    def __init__(self):
        self.ferramentas = QDialog()
        self.ferramentas.setFixedSize(QSize(700, 650))
        self.ferramentas.setWindowTitle('GCrypter')
        self.ferramentas.setWindowIcon(QIcon('gcr-icons/favicon-192x192.png'))
        self.ferramentas.setStyleSheet(theme)

        # layout
        layout = QVBoxLayout()

        # menu-bar
        menu = QMenuBar()
        layout.setMenuBar(menu)
        detalhes = menu.addMenu('&Ajuda')

        lang = detalhes.addAction('&Idioma')
        lang.triggered.connect(self._lang)

        instr = detalhes.addAction('&Instruções')
        instr.triggered.connect(self._instr)
        detalhes.addSeparator()

        sair = detalhes.addAction('&Sair')
        sair.triggered.connect(self._sair)

        sobre = menu.addAction('&Sobre')
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
        website.setToolTip('Acesse o website oficial da ArtesGC!')
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
        layout1.addRow("Criada:", QLabel(f"<b>{_created}</b>"))
        layout1.addRow("Ultimo Início de Sessão:", QLabel(f"<b>{_lastlogin}</b>"))

        inicio_botao = QPushButton("Iniciar")
        inicio_botao.setDefault(True)
        inicio_botao.clicked.connect(inicio)
        terminar_botao = QPushButton("Terminar")
        terminar_botao.clicked.connect(terminar)
        layout2.addWidget(inicio_botao)
        layout2.addWidget(terminar_botao)
        layout1.addRow(layout2)

        moldura.setLayout(layout1)
        return moldura

    # menu-functions
    def _sair(self):
        resp = QMessageBox.question(self.ferramentas, 'Terminar o Programa', 'Obrigado por usar o nosso programa.\n'
                                                                             'Por favor considere visitar a nossa pagina e conhecer outras opções e serviços! - ArtesGC')
        if resp == QMessageBox.StandardButton.Yes:
            open_new('https://artesgc.home.blog')
        else:
            exit(0)

    def _sobre(self):
        QMessageBox.information(self.ferramentas, "Sobre", """<ul>
<li>Nome: GCrypter</li>
<li>Versão: 0.9-112021</li>
<li>Designer & Programador: Nurul-GC</li>
<li>Empresa: ArtesGC, Inc.</li>
</ul>""")

    def _instr(self):
        QMessageBox.information(self.ferramentas, "Instruções", """
Olá, Seja Bem-Vindo ao GCrypter<br>
Ele é uma ferramenta útil e prática para quem gosta de manter os seus arquivos<br>
muito bem protegidos sem ter que se preocupar<br>
com possíveis invasões ou até divulgações indesejadas..

<ul>
<li>O GCrypter lhe oferece opções e um ambiente simples<br>
para que você como utilizador final possa registrar os seus pensamentos,<br>
dados e anotações, guardando-os posteriormente CODIFICADOS..</li>
<li>Nele também está a opção de DECODIFICAÇÂO dos mesmos arquivos..</li>
<li>E até a opção de EDIÇÂO dos arquivos já codificados..</li>
</ul>

Muito Obrigado Pelo Apoio!<br>
Faça Bom Proveito!<br><br>

© 2019-2021 Nurul-GC<br>
™ ArtesGC, Inc.
""")

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
                QMessageBox.information(self.ferramentas, 'Sucessso', 'O idioma definido será carregado após o reinício do programa!')
                janela.close()
            except Exception as erro:
                QMessageBox.warning(self.ferramentas, 'Aviso', f'Enquanto processava o seu pedido, o seguinte erro foi encontrado:\n- {erro}')

        janela = QDialog(self.ferramentas)
        janela.setWindowTitle('Idioma')
        janela.setFixedSize(QSize(300, 200))
        layout = QVBoxLayout()

        labelInfo = QLabel('<h3>Escolha o idioma:</h3>')
        layout.addWidget(labelInfo)

        idiomas = ['Portugues', 'English']
        escolha_idioma = QComboBox()
        escolha_idioma.addItems(idiomas)
        layout.addWidget(escolha_idioma)

        btnSalvar = QPushButton('Salvar')
        btnSalvar.clicked.connect(alterar)
        layout.addWidget(btnSalvar)

        janela.setLayout(layout)
        janela.show()

    # janelas
    def cadastro(self):
        janela_cadastro = QDialog(self.ferramentas)
        janela_cadastro.setWhatsThis('Cadastro: permite ao usuario personalizar uma conta com nome e senha!')
        janela_cadastro.setWindowTitle('Cadastro')

        layout = QFormLayout()

        def guardar():
            if utilizador_cd.text() == '' or codigo.text() == '':
                QMessageBox.warning(self.ferramentas, 'Cadastro', 'Você Deve Preencher os Seus Dados Antes de Entrar..')
            else:
                if codigo.text() != codigo1.text():
                    QMessageBox.warning(self.ferramentas, 'Cadastro', f'Lamento {utilizador_cd.text()} os Códigos Não Correspondem..')
                else:
                    makedirs(f'{debugpath()}/G6r-{utilizador_cd.text()}', exist_ok=True)
                    with open(f'{debugpath()}/G6r-{utilizador_cd.text()}/utilizador.log', 'w+') as file_user:
                        texto = f"""NOME: {utilizador_cd.text()}
SENHA: {codigo.text()}
RESPOSTA: {resposta.text()}"""
                        doc1, doc2 = encrypt(texto)
                        file_user.write(str(doc1) + '\n' + str(doc2))
                    created(_username=utilizador_cd.text())
                    janela_cadastro.destroy(True, True)
                    QMessageBox.information(self.ferramentas, 'Cadastro',
                                            f"Parabens {utilizador_cd.text()} o seu cadastro foi bem sucedido\n"
                                            f"agora inicie sessão para disfrutar do programa..")

        image = QLabel()
        image.setPixmap(QPixmap("gcr-icons/01.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)

        utilizador_cd = QLineEdit()
        utilizador_cd.setToolTip('Obrigatório')
        utilizador_cd.setPlaceholderText('Digite o Seu Nome..')
        layout.addRow(utilizador_cd)

        codigo = QLineEdit()
        codigo.setEchoMode(codigo.EchoMode.PasswordEchoOnEdit)
        codigo.setClearButtonEnabled(True)
        codigo.setToolTip('Obrigatório')
        codigo.setPlaceholderText('Digite a Sua Senha..')
        layout.addRow(codigo)

        codigo1 = QLineEdit()
        codigo1.setEchoMode(codigo1.EchoMode.PasswordEchoOnEdit)
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

        janela_cadastro.setLayout(layout)
        janela_cadastro.show()

    def recuperar_senha(self):
        janela_recuperar_senha = QDialog(self.ferramentas)
        janela_recuperar_senha.setWhatsThis("Sobre: Recuperação da sessão do úsuario!\n"
                                            "Poderá sempre iniciar sessão atravez desta opção caso esqueça permanentemente a sua senha..")
        janela_recuperar_senha.setWindowTitle('Recuperar Senha')

        layout = QFormLayout()

        image = QLabel()
        image.setPixmap(QPixmap("gcr-icons/01.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
                with open(f'{debugpath()}/G6r-{nome.text()}/utilizador.log', 'r+') as file_user:
                    file_ = file_user.readlines()
                    file = decrypt(int(file_[0]), int(file_[1]))
                    if nome.text() in file and resposta.text() in file:
                        logged(_username=nome.text())
                        janela_recuperar_senha.destroy(True, True)
                        self.tab.removeTab(self.tab.currentIndex())
                        return self._principal()
                    else:
                        question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                        f"Lamento {nome.text()} a sua Resposta está Errada ou Você Ainda Não Tem Uma Conta Criada..\n"
                                                        f"Registre-se Para Continuar Usando o Programa!")
                        if question == QMessageBox.StandardButton.Yes:
                            janela_recuperar_senha.destroy(True, True)
                            self.cadastro()
                        elif question == QMessageBox.StandardButton.No:
                            return exit(0)
            except FileNotFoundError:
                question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                f"Lamento {nome.text()} Você Ainda Não Tem Uma Conta Criada..\n"
                                                f"Registre-se Para Continuar Usando o Programa!")
                if question == QMessageBox.StandardButton.Yes:
                    janela_recuperar_senha.destroy(True, True)
                    self.cadastro()
                elif question == QMessageBox.StandardButton.No:
                    return exit(0)

        confirmar = QPushButton('Confirmar')
        confirmar.setDefault(True)
        confirmar.clicked.connect(iniciar)
        layout.addRow(confirmar)

        janela_recuperar_senha.setLayout(layout)
        janela_recuperar_senha.show()

    # molduras
    def usuarios_cadastrados(self):
        moldura_usuarios_cadastrados = QFrame()
        self.tab.addTab(moldura_usuarios_cadastrados, 'Usuarios Registrados')

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
        moldura_inicio_sessao = QFrame()
        self.tab.addTab(moldura_inicio_sessao, 'Inicio Sessão')

        layout = QFormLayout()

        image = QLabel()
        image.setPixmap(QPixmap("gcr-icons/01.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)

        def iniciar():
            try:
                with open(f'{debugpath()}/G6r-{utilizador_is.text()}/utilizador.log', 'r+') as file_user:
                    file_ = file_user.readlines()
                    file = decrypt(int(file_[0]), int(file_[1]))
                    if utilizador_is.text() in file and codigo.text() in file:
                        self.tab.removeTab(self.tab.currentIndex())
                        self.utilizador = utilizador_is.text()
                        logged(_username=self.utilizador)
                        return self._principal()
                    else:
                        question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                        f'Lamento {utilizador_is.text()} Você Ainda Não Tem Uma Conta Criada..\n'
                                                        f'Registre-se Para Continuar Usando o Programa!')
                        if question == QMessageBox.StandardButton.Yes:
                            self.cadastro()
                        elif question == QMessageBox.StandardButton.No:
                            return exit(0)
            except FileNotFoundError:
                question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                f'Lamento {utilizador_is.text()} Você Ainda Não Tem Uma Conta Criada..\n'
                                                f'Registre-se Para Continuar Usando o Programa!')
                if question == QMessageBox.StandardButton.Yes:
                    self.cadastro()
                elif question == QMessageBox.StandardButton.No:
                    return exit(0)

        utilizador_is = QLineEdit()
        utilizador_is.setToolTip('Obrigatório')
        utilizador_is.setPlaceholderText('Digite o Seu Nome..')
        layout.addRow(utilizador_is)

        codigo = QLineEdit()
        codigo.setEchoMode(codigo.EchoMode.PasswordEchoOnEdit)
        codigo.setClearButtonEnabled(True)
        codigo.setToolTip('Obrigatório')
        codigo.returnPressed.connect(iniciar)
        codigo.setPlaceholderText('Digite a Sua Senha..')
        layout.addRow(codigo)

        recuperar_senha = QLabel('<a href="#" style="text-decoration:none; color: white;">Esqueceu a sua senha?</a>')
        recuperar_senha.setToolTip('Permite-lhe recuperar o seu login atravez da sua resposta especial fornecida no cadastro\nCaso ainda não tenha feito o cadastro, fá-lo já!')
        recuperar_senha.linkActivated.connect(self.recuperar_senha)
        recuperar_senha.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(recuperar_senha)

        iniciar_botao = QPushButton('Entrar')
        iniciar_botao.clicked.connect(iniciar)
        iniciar_botao.setDefault(True)
        layout.addRow(iniciar_botao)

        cadastro_botao = QPushButton('Cadastrar')
        cadastro_botao.clicked.connect(self.cadastro)
        layout.addRow(cadastro_botao)

        moldura_inicio_sessao.setLayout(layout)

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
        self.tab.addTab(self.moldura_principal, 'Bem-Vindo')
        self.tab.setCurrentWidget(self.moldura_principal)

        layout = QFormLayout()

        intro = QLabel('<h3><i>"Mesmo que nada esteje bem, certifica-te que tudo corra bem..<br>'
                       'DEUS TE OFERECEU MAIS UM DIA, APROVEITE AO MAXIMO!"</i></h3>')
        intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(intro)

        image = QLabel()
        image.setPixmap(QPixmap('gcr-icons/02.jpg'))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)

        rotulo = QLabel('<h2>Selecione uma Operação a Executar</h2>')
        rotulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(rotulo)

        vis_botao = QPushButton('Pré-visualizar Criptografia')
        vis_botao.clicked.connect(self._visualizar)
        layout.addRow(vis_botao)

        cod_botao = QPushButton('Codificar')
        cod_botao.clicked.connect(self._codificar)
        layout.addRow(cod_botao)

        dec_botao = QPushButton('Decodificar')
        dec_botao.clicked.connect(self._decodificar)
        layout.addRow(dec_botao)

        editar_botao = QPushButton('Editar')
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
            if titulo.text() == '':
                QMessageBox.critical(self.ferramentas, 'Falha', f"Lamento {self.utilizador}, "
                                                                "por favor atribua um nome ao documento antes de guarda-lo!")
            else:
                makedirs(f'{debugpath()}/G6r-{self.utilizador}/docs', exist_ok=True)
                with open(f'{debugpath()}/G6r-{self.utilizador}/docs/{titulo.text()}.gc', 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(f"{doc1}\n{doc2}")
                QMessageBox.information(self.ferramentas, 'Concluido', 'Codificação Bem Sucedida..')
                self.tab.removeTab(self.tab.currentIndex())
                self._principal()

        def textEdited():
            if texto.toPlainText().isascii():
                a, b = encrypt(texto.toPlainText())
                texto_enc.setText(f"{a}\n{b}")
            else:
                texto_enc.clear()

        self.moldura_codificar = QFrame()
        self.tab.addTab(self.moldura_codificar, 'Novo Arquivo')
        self.tab.setCurrentWidget(self.moldura_codificar)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        headlayout = QFormLayout()
        titulo = QLineEdit()
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setToolTip('Obrigatório')
        titulo.setPlaceholderText('Digite um nome para o Arquivo..')

        preview = QRadioButton('Previsualizar Encriptação')
        preview.clicked.connect(pe)

        headlayout.addRow(preview, titulo)
        layout.addLayout(headlayout)

        texto = QTextEdit()
        texto.setFont(QFont('Abel', 10))
        texto.setAcceptRichText(True)
        texto.setAcceptDrops(True)
        texto.textChanged.connect(textEdited)
        texto.setPlaceholderText(f'Em que estas a pensar {self.utilizador}..')
        layout.addWidget(texto)

        texto_enc = QTextEdit()
        texto_enc.setReadOnly(True)
        texto_enc.setHidden(True)
        texto_enc.setAcceptDrops(True)
        texto_enc.setPlaceholderText(f'O seu texto codificado será apresentado aqui..')
        layout.addWidget(texto_enc)

        footlayout = QHBoxLayout()
        guardar_botao = QPushButton('Guardar')
        guardar_botao.setToolTip('Codificado')
        guardar_botao.clicked.connect(guardar)
        guardar_botao.setDefault(True)
        footlayout.addWidget(guardar_botao)

        cancelar = lambda p: self.tab.removeTab(self.tab.currentIndex())
        cancelar_botao = QPushButton('Cancelar')
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
        nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'{debugpath()}/G6r-{self.utilizador}/docs', filter='Ficheiros (*.gc)', caption='Selecione o arquivo')
        try:
            with open(nome_file_open[0], 'r+') as file_decod:
                file_ = file_decod.readlines()
                file = decrypt(file_[0], file_[1])

            self.moldura_decodificar = QFrame()
            self.tab.addTab(self.moldura_decodificar, 'Lendo Arquivo')
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

            fechar_botao = QPushButton('Fechar')
            fechar_botao.setDefault(True)
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            self.moldura_decodificar.setLayout(layout)
        except FileNotFoundError:
            QMessageBox.warning(self.ferramentas, 'Aviso', 'Ficheiro Não Encontrado ou Processo Cancelado!')

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
        nome_file_open = QFileDialog.getOpenFileName(parent=self.ferramentas, directory=f'{debugpath()}/G6r-{self.utilizador}/docs', filter='Ficheiros (*.gc)', caption='Selecione o arquivo')
        try:
            with open(nome_file_open[0], 'r+') as file_decod:
                file_ = file_decod.readlines()
                file = decrypt(file_[0], file_[1])

            self.moldura_editar = QFrame()
            self.tab.addTab(self.moldura_editar, 'Editando Arquivo')
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
                QMessageBox.information(self.ferramentas, 'Concluido', 'Codificação Bem Sucedida 👌...')
                self.tab.removeTab(self.tab.currentIndex())
                self._principal()

            guardar_botao = QPushButton('Salvar')
            guardar_botao.setToolTip('Recodificado')
            guardar_botao.clicked.connect(guardar)
            layout.addWidget(guardar_botao)

            def fechar():
                with open(nome_file_open[0], 'w+') as file_enc:
                    doc1, doc2 = encrypt(texto.toPlainText())
                    file_enc.write(str(doc1) + '\n' + str(doc2))
                self.tab.removeTab(self.tab.currentIndex())

            fechar_botao = QPushButton('Fechar')
            fechar_botao.setDefault(True)
            fechar_botao.clicked.connect(fechar)
            layout.addWidget(fechar_botao)
            self.moldura_editar.setLayout(layout)
        except FileNotFoundError:
            QMessageBox.warning(self.ferramentas, 'Aviso', 'Ficheiro Não Encontrado ou Processo Cancelado!')

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
        self.tab.addTab(self.moldura_visualizar, 'Pré-visualizando criptografia')
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
                        QMessageBox.critical(self.ferramentas, 'Erro de codificação', 'Verifique se os valores inseridos estão corretos..')
                        rtext.clear()
                else:
                    a, b = encrypt(ptext.toPlainText())
                    rtext.setText(f"{a}\n{b}")

        ptext = QTextEdit()
        ptext.setPlaceholderText(f"Digite alguma coisa {self.utilizador}..")
        ptext.textChanged.connect(textEdited)
        layoutText.addWidget(ptext)

        rtext = QTextEdit()
        rtext.setPlaceholderText("E o resultado sera transcrito aqui..")
        rtext.setReadOnly(True)
        layoutText.addWidget(rtext)
        layout.addRow(layoutText)

        infoLabel = QLabel("""
<small>
<ul>
<li>Este recurso permite que você teste e entenda como o GCrypter funciona.</li>
<li>Você também pode copiar e colar valores de uma caixa para outra.</li>
<li>Sinta-se à vontade para tentar criptografar e descriptografar o que quiser.</li>
</ul>
</small>""")
        layout.addRow(infoLabel)

        fechar = lambda: self.tab.removeTab(self.tab.currentIndex())
        fechar_botao = QPushButton('Fechar')
        fechar_botao.setDefault(True)
        fechar_botao.clicked.connect(fechar)
        layout.addRow(fechar_botao)

        self.moldura_visualizar.setLayout(layout)
