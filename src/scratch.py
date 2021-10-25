# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
# ******************************************************************************

def verificarData(frase: str):
    """funcao para extrair a data de um texto
    {datetime.today(datetime.date())}
    """
    data = ""
    dataRegex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    confirma = dataRegex.search(frase)
    if confirma:
        data = confirma.group()
    return data
