# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
# ******************************************************************************
from datetime import datetime
from os import name, path
from re import compile
from subprocess import getoutput


def debugpath() -> str:
    if name == 'posix':
        home = getoutput('echo $HOME')
        return path.join(home, '.g6r-debug')
    return '.g6r-debug'


def perfilnome(_folder: str) -> str or None:
    nome = compile("G6r-[aA-zZ]+")
    if nome.match(_folder):
        return _folder.split("-")[-1]
    return None


def created(_username: str):
    from g6r.db import G6RDB
    db = G6RDB()
    date_created = datetime.today()
    return db.insert_user(_nome=_username, _created=date_created)


def logged(_username: str):
    from g6r.db import G6RDB
    db = G6RDB()
    date_last_login = datetime.today()
    return db.update_lastlogin(_nome=_username, _last_login=date_last_login)


def localpath() -> str:
    return path.abspath(path.curdir)


def after(_sec: int, _do):
    n = 0
    while n < _sec:
        n += 1
    return _do
