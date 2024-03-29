import sqlite3
from g6r.gfuns import debugpath


class G6RDB:
    """classe para gerir as operacoes com a db"""

    def connect_db(self):
        connection = None
        try:
            connection = sqlite3.connect(f"{debugpath()}/gcrypter.db")
        except Exception:
            connection = False
        return connection

    def create_table(self, _sql_value):
        db = self.connect_db()
        try:
            executor = db.cursor()
            resultado = executor.execute(_sql_value)
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar a db!\nconnection_result:{db}')

    def insert_user(self, _nome=None, _created=None):
        db = self.connect_db()
        sql_value = "CREATE TABLE IF NOT EXISTS users" \
                    "(id integer primary key autoincrement," \
                    " nome varchar(20) not null," \
                    " created varchar(30)," \
                    " last_login varchar(30));"
        self.create_table(_sql_value=sql_value)
        try:
            if _nome and _created:
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

    def update_config(self, _lang=None, _theme=None):
        db = self.connect_db()
        sql_value = "CREATE TABLE IF NOT EXISTS config" \
                    "(id integer primary key," \
                    " lang varchar(20) not null," \
                    " theme varchar(10) not null);"
        try:
            self.create_table(_sql_value=sql_value)
            executor = db.cursor()
            if _lang and _theme:
                if len(self.return_data(_table='config')) >= 1:
                    resultado = executor.execute("UPDATE config SET lang=?, theme=? "
                                                 "WHERE id=1;", (_lang, _theme))
                else:
                    resultado = executor.execute("INSERT INTO config (lang, theme) "
                                                 "VALUES (?,?);", (_lang, _theme))

                if resultado:
                    db.commit()
                    db.close()
        except Exception as erro:
            print(erro)
        if not db:
            raise ConnectionError(f"Erro ao conectar a db!\nconnection_result:{db}")
        return True

    def update_lastlogin(self, _nome, _last_login):
        db = self.connect_db()
        try:
            executor = db.cursor()
            resultado = executor.execute("UPDATE users SET last_login=?"
                                         "WHERE nome=?;", (_last_login, _nome))
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f"Erro ao conectar a db!\nconnection_result:{db}")

    def return_data(self, _table, _nome=None):
        resultado = None
        db = self.connect_db()
        executor = db.cursor()
        if _nome:
            resultado = executor.execute("SELECT * FROM users WHERE nome=?;", (_nome,))
        else:
            resultado = executor.execute(f"SELECT * FROM {_table};")
        if resultado:
            return executor.fetchall()
        if not db:
            raise ConnectionError(f'Erro ao conectar a db!\nconnection_result:{db}')

    def delete_data(self, _nome):
        db = self.connect_db()
        try:
            executor = db.cursor()
            resultado = executor.execute("DELETE FROM users WHERE nome=?;", (_nome,))
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar a db!\nconnection_result:{db}')
