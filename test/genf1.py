# codigo que genera fechas aleatorias posibles
# https://realpython.com/python-random/
# https://mkaz.blog/code/python-string-format-cookbook/
# https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python/16870699
# https://random-date-generator.com/

import random
import datetime

lmeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
          'noviembre', 'diciembre']

lmesesi = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
           'december']


def validaFecha(fecha):
    year, month, day = fecha.split('-')

    isvaliddate = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isvaliddate = False

    return isvaliddate


def genfecharand():
    bgen = True

    while bgen:
        nmes = random.randint(0, 11)

        mes = lmeses[nmes]
        nmes += 1

        dia = random.randint(1, 31)
        anno = random.randint(1900, 2050)

        fecha = f'{dia} de {mes} del {anno}'

        nmesf = "{:0>2d}".format(nmes)
        diaf = "{:0>2d}".format(dia)

        fi = f'{anno}-{nmesf}-{diaf}'

        if validaFecha(fi):
            bgen = False

    return fecha, fi


def genfecharandi():
    bgen = True

    while bgen:
        nmes = random.randint(0, 11)

        mes = lmesesi[nmes]
        nmes += 1

        dia = random.randint(1, 31)
        anno = random.randint(1900, 2050)

        fecha = f'{dia} {mes} {anno}'

        nmesf = "{:0>2d}".format(nmes)
        diaf = "{:0>2d}".format(dia)

        fi = f'{anno}-{nmesf}-{diaf}'

        if validaFecha(fi):
            bgen = False

    return fecha, fi


def genfecharand2():
    bgen = True

    while bgen:
        nmes = random.randint(1, 12)
        dia = random.randint(1, 31)
        anno = random.randint(1900, 2050)

        nmesf = "{:0>2d}".format(nmes)
        diaf = "{:0>2d}".format(dia)

        fecha = f'{anno}{nmesf}{diaf}'
        fi = f'{anno}-{nmesf}-{diaf}'

        if validaFecha(fi):
            bgen = False

    return fecha, fi


def genfecharand3():
    bgen = True

    nformat = random.randint(0, 1E6)

    lsep = ['-', '/', ' ']

    while bgen:
        nmes = random.randint(1, 12)
        dia = random.randint(1, 31)
        anno = random.randint(1900, 2050)

        nmesf = "{:0>2d}".format(nmes)

        if nformat % 156 == 0:
            nmesf = nmes

        if nformat % 497 == 0:
            diaf = "{:0>2d}".format(dia)
        else:
            diaf = dia

        sep = random.choice(lsep)

        if nformat % 3 == 0:
            fecha = f'{anno}{sep}{nmesf}{sep}{diaf}'
        elif nformat % 3 == 1:
            fecha = f'{diaf}{sep}{nmesf}{sep}{anno}'
        else:
            fecha = f'{nmesf}{sep}{diaf}{sep}{anno}'

        diaf = "{:0>2d}".format(dia)
        fi = f'{anno}-{nmesf}-{diaf}'

        if validaFecha(fi):
            bgen = False

    return fecha, fi


print(genfecharand())
print(genfecharandi())
print(genfecharand2())
print(genfecharand3())
