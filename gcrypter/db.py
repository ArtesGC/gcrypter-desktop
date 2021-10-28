import sqlite3

from gcrypter.globalfunc import debugpath


class G6RDB:
    """classe para gerir as operacoes com a db"""

    def conectar_db(self):
        db = None
        try:
            db = sqlite3.connect(f"{debugpath()}/gcrypter.db")
            executor = db.cursor()
            resultado = executor.execute(
                "CREATE TABLE IF NOT EXISTS users"
                "(id integer primary key autoincrement,"
                " nome varchar(20) not null,"
                " created varchar(30),"
                " last_login varchar(30));"
            )
            if resultado:
                db.commit()
        except Exception as erro:
            db = erro
        return db

    def apagar_dado(self, _nome: str):
        db = self.conectar_db()
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
            raise ConnectionError(f'Erro ao conectar a db!\nconnection_result:{db}')

    def atualizar_created(self, _nome, _created):
        db = self.conectar_db()
        try:
            executor = db.cursor()
            resultado = executor.execute('INSERT INTO users (nome, created) '
                                         'VALUES (?, ?);', (_nome, _created))
            if resultado:
                db.commit()
                db.close()
        except Exception as erro:
            print(erro)
        if not db:
            raise ConnectionError(f'Erro ao conectar a db!\nconnection_result:{db}')
        return True

    def atualizar_lastlogin(self, _nome, _last_login):
        db = self.conectar_db()
        try:
            executor = db.cursor()
            resultado = executor.execute("UPDATE users SET last_login=?"
                                         "WHERE nome=?", (_last_login, _nome))
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar a db!\nconnection_result:{db}')

    def retornar_dados(self, _nome=None):
        resultado = None
        db = self.conectar_db()
        try:
            executor = db.cursor()
            if _nome:
                resultado = executor.execute("SELECT * FROM users WHERE nome=?", (_nome,))
            else:
                resultado = executor.execute("SELECT * FROM users")
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar a db!\nconnection_result:{db}')
        elif resultado:
            dados = executor.fetchall()
            return dados
