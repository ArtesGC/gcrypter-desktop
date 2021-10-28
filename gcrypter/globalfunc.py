# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
# ******************************************************************************
from configparser import ConfigParser
from datetime import datetime
from os import path
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
        return path.join(home, '.gcr-debug')
    return '.gcr-debug'


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


def localpath() -> str:
    return path.abspath(path.curdir)
