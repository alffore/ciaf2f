import random
import datetime
import time

lmeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
          'noviembre', 'diciembre']

lmesesi = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
           'december']


def validafecha(fecha):
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

        if validafecha(fi):
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

        if validafecha(fi):
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

        if validafecha(fi):
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

        if validafecha(fi):
            bgen = False

    return fecha, fi


if __name__ == '__main__':

    start = time.perf_counter()
    with open('../data/fechas_train.csv', "w") as wf:
        wf.write('fecha,fi\n')
        for _ in range(1000000):
            nmodo = random.randint(0, 1E10)

            if nmodo % 4 == 0:
                fecha, fi = genfecharand()
            elif nmodo % 4 == 1:
                fecha, fi = genfecharandi()
            elif nmodo % 4 == 2:
                fecha, fi = genfecharand2()
            else:
                fecha, fi = genfecharand3()
            wf.write(f'{fecha},{fi}\n')

    with open('../data/fechas_test.csv', "w") as wf:
        wf.write('fecha,fi\n')
        for _ in range(250000):
            nmodo = random.randint(0, 1E10)

            if nmodo % 4 == 0:
                fecha, fi = genfecharand()
            elif nmodo % 4 == 1:
                fecha, fi = genfecharandi()
            elif nmodo % 4 == 2:
                fecha, fi = genfecharand2()
            else:
                fecha, fi = genfecharand3()
            wf.write(f'{fecha},{fi}\n')

    print(f'Termino en {round(time.perf_counter() - start, 2)} segundos')
