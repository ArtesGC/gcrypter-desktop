import sqlite3

from gcrypter import debugpath


class G6RDB:
    """classe para gerir as operacoes com a db"""

    def conectarDb(self):
        db = None
        try:
            db = sqlite3.connect(f'{debugpath()}/gc.db')
            executor = db.cursor()
            resultado = executor.execute(
                "CREATE TABLE IF NOT EXISTS users"
                "(id integer primary key autoincrement,"
                " nome varchar(20) not null,"
                " created varchar(30) not null,"
                " last_login varchar(30) not null);"
            )
            if resultado:
                db.commit()
        except Exception:
            db = False
        return db

    def apagarDado(self, _nome: str):
        db = self.conectarDb()
        try:
            executor = db.cursor()
            resultado = executor.execute("DELETE FROM users WHERE nome=?", (_nome,))
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar db!\nconnection_result:{db}')

    def adicionarDados(self, _nome, _created, _last_login):
        db = self.conectarDb()
        try:
            executor = db.cursor()
            resultado = executor.execute('INSERT INTO gcontactos (nome, numero, last_login) VALUES(?, ?, ?, ?);',
                                         (_nome, _created, _last_login))
            if resultado:
                db.commit()
                db.close()
        except Exception as erro:
            print(erro)
        if not db:
            raise ConnectionError(f'Erro ao conectar db!\nconnection_result:{db}')
        return True

    def atualizarDados(self, _id, _nome, _numero, _email, _morada):
        db = self.conectarDb()
        try:
            executor = db.cursor()
            resultado = executor.execute("UPDATE gcontactos "
                                         "SET nome=?, numero=?, email=?, morada=?"
                                         "WHERE id=?", (_nome, _numero, _email, _morada, _id))
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar db!\nconnection_result:{db}')

    def retornarDados(self, _nome=None):
        resultado = None
        db = self.conectarDb()
        try:
            executor = db.cursor()
            if _nome:
                resultado = executor.execute("SELECT * FROM gcontactos WHERE nome=?", (_nome,))
            else:
                resultado = executor.execute("SELECT * FROM gcontactos")
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar db!\nconnection_result:{db}')
        elif resultado:
            dados = executor.fetchall()
            return dados
