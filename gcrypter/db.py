import sqlite3
from gcrypter.globalfunc import debugpath


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

    def insert_user(self, _nome, _created):
        db = self.connect_db()
        sql_value = "CREATE TABLE IF NOT EXISTS users" \
                    "(id integer primary key autoincrement," \
                    " nome varchar(20) not null," \
                    " created varchar(30)," \
                    " last_login varchar(30));"
        self.create_table(_sql_value=sql_value)
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

    def update_config(self, _lang):
        db = self.connect_db()
        sql_value = "CREATE TABLE IF NOT EXISTS config" \
                    "(id integer primary key," \
                    " lang varchar(20) not null);"
        try:
            self.create_table(_sql_value=sql_value)
            executor = db.cursor()
            if len(self.return_data(_table='config')) >= 1:
                resultado = executor.execute("UPDATE config SET lang=? "
                                             "WHERE id=1;", (_lang,))
            else:
                resultado = executor.execute("INSERT INTO config (lang) "
                                             "VALUES (?);", (_lang,))

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
        try:
            executor = db.cursor()
            if _nome:
                resultado = executor.execute("SELECT * FROM users WHERE nome=?;", (_nome,))
            else:
                resultado = executor.execute(f"SELECT * FROM {_table};")
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar a db!\nconnection_result:{db}')
        elif resultado:
            dados = executor.fetchall()
            return dados

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


if __name__ == '__main__':
    _db = G6RDB()
    print(_db.return_data(_table='users'))
