from unicodedata import normalize
import datetime
import re
import string
import random

DATA_INTERNACIONAL = re.compile(r'(\d{4})[/-]{1}(\d{2})[/-]{1}(\d{2})')
VALOR_MONETARIO = re.compile(r'(\d+)[\.\,]{1}(\d{2})')

"""
Função que troca a vírgula por ponto para fazer operações de calcular,
pois os campos VALOR são todos do tipo CHARFIELD
"""
def change_comma_by_dot(number):
    return number.replace(",", ".")

def random_string(size=250):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def remover_separadores(valor):
    return ''.join(filter(lambda x: x.isdigit(), valor))


def split_by(valor, separadores=(' ', '-', '_', '/', '=')):
    a = ''
    index = 0
    while not a:
        try:
            a, b = valor.split(separadores[index])
            return remover_separadores(a), remover_separadores(b)
        except ValueError:
            a = ''
            index += 1
        except IndexError:
            return valor


def split_fone(value):
    if len(value) > 11:
        valor = remover_separadores(remover_acentos(value))
    elif len(value) > 10:
        valor = split_by(value)
    else:
        valor = remover_separadores(remover_acentos(value))

    if isinstance(valor, tuple):
        return valor
    elif isinstance(valor, str):
        # checa tamanho
        if len(valor) < 9:
            return '', ''
        elif len(valor) < 10:
            return '', valor
        elif len(valor) < 11:
            return valor[:2], valor[2:11]
        elif len(valor) == 11:
            return valor[:2], valor[2:11]
        else:
            raise ValueError
    else:
        raise ValueError


def format_date_br(data):
    if '/' in data:
        ano, mes, dia = [int(i) for i in data.split('/')]
    elif '-' in data:
        ano, mes, dia = [int(i) for i in data.split('-')]
    else:
        raise AttributeError('O Tipo data não contém um separador conhecido')

    return datetime.date(ano, mes, dia)

def convert_date(data):
    try:
        if '/' in data:
            ano, mes, dia = [int(i) for i in data.split('/')]
        elif '-' in data:
            ano, mes, dia = [int(i) for i in data.split('-')]
        return datetime.date(ano, mes, dia)
    except:
        return None


def test_if_exists_field(context):
    try:
        return format_date_br(context['description']['data_do_comunicado_do_desligamento'])
    except:
        return None


def format_values(item):
    if isinstance(item[1], str):
        if DATA_INTERNACIONAL.fullmatch(item[1]):
            return item[0], datetime.date(*[int(i) for i in DATA_INTERNACIONAL.fullmatch(item[1]).groups()])
        elif VALOR_MONETARIO.fullmatch(item[1]):
            return item[0], 'R$ {}'.format(','.join(VALOR_MONETARIO.fullmatch(item[1]).groups()))
        else:
            return item
    elif isinstance(item[1], int) or isinstance(item[1], list):
        return item
    elif isinstance(item[1], dict):
        new_seq = dict(map(format_values, item[1].items()))
        return item[0], new_seq
    else:
        raise TypeError('O tipo {} não é suportado'.format(type(item[1])))
