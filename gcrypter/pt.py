# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
# ******************************************************************************
from os import makedirs, listdir
from webbrowser import open_new

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from gcrypter.db import G6RDB
from gcrypter.gfuns import debugpath, encrypt, decrypt, created, logged, localpath


class PT:
    def __init__(self):
        self.ferramentas = QDialog()
        self.ferramentas.setFocus()
        self.ferramentas.setFixedSize(QSize(450, 450))
        self.ferramentas.setWindowTitle('GCrypter')
        self.ferramentas.setWindowIcon(QIcon(f'{localpath()}/g6r-icons/favicons/favicon-192x192.png'))

        # layout
        layout = QVBoxLayout()

        # menu-bar
        menu = QMenuBar()
        layout.setMenuBar(menu)
        detalhes = menu.addMenu('&Ajuda')

        lang = detalhes.addAction('&Cofigurações')
        lang.triggered.connect(self._config)

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
        self.gdb = G6RDB()
        self.utilizador = None
        self.moldura_editar = None
        self.moldura_principal = None
        self.moldura_codificar = None
        self.moldura_visualizar = None
        self.moldura_decodificar = None

        self.ferramentas.setLayout(layout)
        self.inicio_sessao()

    # getters and setters
    def perfilframe(self, _nome: str, _created: str, _lastlogin: str) -> QFrame:
        def inicio():
            self.tab.removeTab(self.tab.currentIndex())
            return self.inicio_sessao()

        def terminar():
            pass

        moldura = QFrame()
        moldura.setStyleSheet("border-radius: 5px;"
                              "border-color: white;"
                              "border-width: 1px;"
                              "border-style: solid;")

        layout1 = QFormLayout()
        layout_btns = QHBoxLayout()

        layout1.addRow(QLabel(f"<h3>{_nome}</h3>"
                              f"Criada: <b>{_created}</b><br>"
                              f"Ultimo Início de Sessão: <b>{_lastlogin}</b>"))

        inicio_botao = QPushButton("Iniciar")
        inicio_botao.setDefault(True)
        inicio_botao.setStyleSheet("QPushButton:hover{text-decoration: underline;}")
        inicio_botao.clicked.connect(inicio)
        layout_btns.addWidget(inicio_botao)

        terminar_botao = QPushButton("Terminar")
        terminar_botao.setStyleSheet("QPushButton:hover{text-decoration: underline;}")
        terminar_botao.clicked.connect(terminar)
        layout_btns.addWidget(terminar_botao)
        layout1.addRow(layout_btns)

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
<li>Nome: <b>GCrypter</b></li>
<li>Versão: <b>0.9-112021</b></li>
<li>Designer & Programador: <b>Nurul-GC</b></li>
<li>Empresa: <b>ArtesGC, Inc.</b></li>
</ul>""")

    def _instr(self):
        QMessageBox.information(self.ferramentas, "Instruções", """
<h3>Olá, Seja Bem-Vindo ao GCrypter</h3><hr>

Ele é uma ferramenta útil e prática para quem gosta<br>
de manter os seus arquivos muito bem protegidos<br>
sem ter que se preocupar com possíveis invasões<br>
ou até divulgações indesejadas.

<ul>
<li>O <b>GCrypter</b> lhe oferece opções e um ambiente simples<br>
para que você como utilizador final possa registrar os seus pensamentos,<br>
dados e anotações, guardando-os posteriormente <b>CODIFICADOS</b>..</li>
<li>Nele também está a opção de <b>DECODIFICAÇÂO</b> dos mesmos arquivos..</li>
<li>E até a opção de <b>EDIÇÂO</b> dos arquivos já codificados..</li>
</ul>

Muito Obrigado Pelo Apoio!<br>
Faça Bom Proveito!<br><br>

<b>© 2019-2021 Nurul-GC<br>
™ ArtesGC, Inc.</b>
""")

    def _config(self):
        def alterar():
            try:
                self.gdb.update_config(_lang=escolha_idioma.currentText(), _theme=escolha_temas.currentText())
                QMessageBox.information(self.ferramentas, 'Sucessso', 'As modificações definidas serão carregadas após o reinício do programa!')
                janela.close()
            except Exception as erro:
                QMessageBox.warning(self.ferramentas, 'Aviso', f'Enquanto processava o seu pedido, o seguinte erro foi encontrado:\n- {erro}')

        janela = QDialog(self.ferramentas)
        janela.setWindowTitle('Configurações')

        layout = QFormLayout()
        layout.setSpacing(10)

        idiomas = ['Portugues', 'English']
        escolha_idioma = QComboBox()
        escolha_idioma.addItems(idiomas)
        layout.addRow('Escolha o &Idioma:', escolha_idioma)

        temas = ['Light', 'Dark']
        escolha_temas = QComboBox()
        escolha_temas.addItems(temas)
        layout.addRow('Escolha o &Tema:', escolha_temas)

        btnSalvar = QPushButton('Salvar')
        btnSalvar.clicked.connect(alterar)
        layout.addRow(btnSalvar)
        layout.addRow(QLabel('<small><ul><li>O botão para salvar captura ambas as escolhas, '
                             'por favor certifique-se de defini-las antes de pressiona-lo!</li></ul></small>'))

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
                    janela_cadastro.destroy()
                    QMessageBox.information(self.ferramentas, 'Cadastro',
                                            f"Parabens {utilizador_cd.text()} o seu cadastro foi bem sucedido\n"
                                            f"agora inicie sessão para disfrutar do programa..")

        image = QLabel()
        image.setPixmap(QPixmap(f"{localpath()}/g6r-icons/01.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)
        layout.addRow(QLabel("<h3>Preencha os Seus Dados:</h3>"))

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
        image.setPixmap(QPixmap(f"{localpath()}/g6r-icons/01.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(image)
        layout.addRow(QLabel("<h3>Preencha os Seus Dados:</h3>"))

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
                        janela_recuperar_senha.destroy()
                        self.tab.removeTab(self.tab.currentIndex())
                        return self._principal()
                    else:
                        question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                        f"Lamento {nome.text()} a sua Resposta está Errada ou Você Ainda Não Tem Uma Conta Criada..\n"
                                                        f"Registre-se Para Continuar Usando o Programa!")
                        if question == QMessageBox.StandardButton.Yes:
                            janela_recuperar_senha.destroy()
                            self.cadastro()
                        elif question == QMessageBox.StandardButton.No:
                            return exit(0)
            except FileNotFoundError:
                question = QMessageBox.question(self.ferramentas, 'Falha ao Iniciar Sessão',
                                                f"Lamento {nome.text()} Você Ainda Não Tem Uma Conta Criada..\n"
                                                f"Registre-se Para Continuar Usando o Programa!")
                if question == QMessageBox.StandardButton.Yes:
                    janela_recuperar_senha.destroy()
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
        self.tab.addTab(moldura_usuarios_cadastrados, 'Usuarios Cadastrados')

        layout = QVBoxLayout()
        layout.addSpacing(10)
        layout.addWidget(QLabel("<h2>Inicio Rapido:</h2>"))

        if len(self.gdb.return_data(_table='users')) >= 1:
            for user in self.gdb.return_data(_table='users'):
                nomeusuario = user[1]
                criada = user[2]
                lastlogin = user[3]
                layout.addWidget(self.perfilframe(_nome=nomeusuario, _created=criada, _lastlogin=lastlogin))
        else:
            layout.addWidget(QLabel("<i>Ainda sem contas cadastradas...</i>"))

        cadastro_botao = QPushButton('Cadastrar')
        cadastro_botao.clicked.connect(self.cadastro)
        layout.addWidget(cadastro_botao)

        moldura_usuarios_cadastrados.setLayout(layout)

    def inicio_sessao(self):
        moldura_inicio_sessao = QFrame()
        self.tab.addTab(moldura_inicio_sessao, 'Inicio Sessão')

        layout = QFormLayout()
        layout.setSpacing(30)

        layout.addRow(QLabel("<h2>Preencha os Seus Dados<br>Para Iniciar Sessão:</h2>"))

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

        layout_btns = QHBoxLayout()
        iniciar_botao = QPushButton('Entrar')
        iniciar_botao.clicked.connect(iniciar)
        iniciar_botao.setDefault(True)
        layout_btns.addWidget(iniciar_botao)

        cadastro_botao = QPushButton('Cadastrar')
        cadastro_botao.clicked.connect(self.cadastro)
        layout_btns.addWidget(cadastro_botao)
        layout.addRow(layout_btns)

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
        self.ferramentas.setFixedSize(QSize(800, 600))
        self.moldura_principal = QFrame()
        self.tab.addTab(self.moldura_principal, 'Bem-Vindo')
        self.tab.setCurrentWidget(self.moldura_principal)

        layout = QVBoxLayout()

        intro = QLabel('<h3><i>"Mesmo que nada esteje bem, certifica-te que tudo corra bem..<br>'
                       'DEUS TE OFERECEU MAIS UM DIA, APROVEITE AO MAXIMO!"</i></h3>')
        intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(intro)

        image = QLabel()
        image.setPixmap(QPixmap(f'{localpath()}/g6r-icons/02.jpg'))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image)

        rotulo = QLabel('<h2>Selecione uma Operação a Executar</h2>')
        rotulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(rotulo)

        vis_botao = QPushButton('Pré-visualizar Criptografia')
        vis_botao.clicked.connect(self._visualizar)
        layout.addWidget(vis_botao)

        cod_botao = QPushButton('Codificar')
        cod_botao.clicked.connect(self._codificar)
        layout.addWidget(cod_botao)

        dec_botao = QPushButton('Decodificar')
        dec_botao.clicked.connect(self._decodificar)
        layout.addWidget(dec_botao)

        editar_botao = QPushButton('Editar')
        editar_botao.clicked.connect(self._editar)
        layout.addWidget(editar_botao)

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
