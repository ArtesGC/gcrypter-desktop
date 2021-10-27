# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
# ******************************************************************************

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
Version: 0.8.072021
Designer & Programmer: Nurul-GC
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
