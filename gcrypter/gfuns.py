# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
# ******************************************************************************
from datetime import datetime
from os import name, path
from re import compile
from secrets import token_bytes
from subprocess import getoutput


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
    from gcrypter.db import G6RDB
    db = G6RDB()
    date_created = datetime.today()
    return db.insert_user(_nome=_username, _created=date_created)


def logged(_username: str):
    from gcrypter.db import G6RDB
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
