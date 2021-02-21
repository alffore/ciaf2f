import random
import datetime
import time

lmeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
          'noviembre', 'diciembre']

lmeses_reducido = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

lmesesi = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
           'december']

lmesesi_reducido = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

a_min = 1600
a_max = 7500


def validafecha(fecha):
    """

    :param fecha:
    :return:
    """
    year, month, day = fecha.split('-')

    isvaliddate = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isvaliddate = False

    return isvaliddate


def genfecharand():
    bgen = True

    asep = [' de ', ' del ', ' ', '-', '/', ':', "#", "\\", '\'', '']

    while bgen:
        nmes = random.randint(0, 11)

        mes = lmeses_reducido[nmes]
        if random.randint(0, 1E10) % 2 == 0:
            mes = lmeses[nmes]

        nmes += 1

        dia = random.randint(1, 31)
        diamod = random.choice([dia, "{:0>2d}".format(dia)])

        anno = random.randint(a_min, a_max)

        sep1 = random.choice(asep)
        sep2 = random.choice(asep)

        fecha = f'{anno}{sep1}{mes}{sep2}{diamod}'

        if random.randint(0, 1E10) % 2 == 0:
            fecha = f'{diamod}{sep1}{mes}{sep2}{anno}'

        fecha = mutacadena(fecha)

        nmesf = "{:0>2d}".format(nmes)
        diaf = "{:0>2d}".format(dia)

        fi = f'{anno}-{nmesf}-{diaf}'

        if validafecha(fi):
            bgen = False

    return fecha, fi


def genfecharandi():
    bgen = True

    asep = [' ', '-', '/', ':', "#", "\\", '\'', '']

    while bgen:
        nmes = random.randint(0, 11)

        mes = lmesesi_reducido[nmes]
        if random.randint(0, 1E10) % 2 == 0:
            mes = lmesesi[nmes]

        nmes += 1

        dia = random.randint(1, 31)
        anno = random.randint(a_min, a_max)

        mes = mutacadena(mes)
        sep1 = random.choice(asep)
        sep2 = random.choice(asep)

        fecha = f'{dia}{sep1}{mes}{sep2}{anno}'

        if random.randint(0, 1E10) % 2 == 0:
            fecha = f'{anno}{sep1}{mes}{sep2}{dia}'

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
        anno = random.randint(a_min, a_max)

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

    lsep = ['-', '/', ' ', "\\", '', '_']

    while bgen:
        nmes = random.randint(1, 12)
        dia = random.randint(1, 31)
        anno = random.randint(a_min, a_max)

        nmesf = "{:0>2d}".format(nmes)

        if nformat % 156 == 0:
            nmesf = nmes

        diaf = dia
        if nformat % 497 == 0:
            diaf = "{:0>2d}".format(dia)

        sep = random.choice(lsep)
        sep1 = random.choice(lsep)

        if nformat % 4 == 0:
            fecha = f'{anno}{sep}{nmesf}{sep1}{diaf}'
        elif nformat % 4 == 1:
            fecha = f'{diaf}{sep}{nmesf}{sep1}{anno}'
        elif nformat % 4 == 2:
            fecha = f'{nmesf}{sep}{diaf}{sep1}{anno}'
        elif nformat % 4 == 3:
            fecha = f'{diaf}\\{nmesf}\\{anno}'

        diaf = "{:0>2d}".format(dia)
        fi = f'{anno}-{nmesf}-{diaf}'

        if validafecha(fi):
            bgen = False

    return fecha, fi


def genfecharand4():
    bgen = True

    lsep = [' ', '']

    while bgen:
        nmes = random.randint(0, 11)

        mes = lmeses[nmes]
        mesi = lmesesi[nmes]
        mes = random.choice([mes, mesi])

        nmes += 1

        dia = random.randint(1, 31)
        anno = random.randint(a_min, a_max)

        mes = mutacadena(mes)

        sep = random.choice(lsep)
        sep1 = random.choice(lsep)

        fecha = f'{mes}{sep}{dia},{sep1}{anno}'

        nmesf = "{:0>2d}".format(nmes)
        diaf = "{:0>2d}".format(dia)

        fi = f'{anno}-{nmesf}-{diaf}'

        if validafecha(fi):
            bgen = False

    return fecha, fi


def genfecharand5():
    bgen = True

    while bgen:

        anno = random.randint(a_min, a_max)

        fecha = f'{anno}'

        fi = f'{anno}-01-01'

        if validafecha(fi):
            bgen = False

    return fecha, fi


def mutacadena(cadena):
    c = random.randint(1, 1E9)
    cl = "a1bc(/de2f3gh,i4jk6lm5n7ñop8qr9s.tuvw0xyz )?"
    cm = cl[random.randint(0, len(cl) - 1)]
    posm = random.randint(0, len(cadena) - 1)
    aux = []
    if c % 13 == 0:
        for i in range(len(cadena)):
            if i == posm:
                if c % 2 == 0:
                    aux.append(cm)
            else:
                aux.append(cadena[i])
    elif c % 13 == 5:
        for i in range(len(cadena)):
            if i == posm and c%3 == 0:
                aux.append(cm)
                aux.append(cadena[i])
            else:
                aux.append(cadena[i])

    if len(aux) > 0:
        cadena = ''.join(aux)
    return cadena


if __name__ == '__main__':
    print("Generador de fechas aleatorias")

    ntrain = 2000000
    ntest = 100000
    max_length = 0

    start = time.perf_counter()
    with open('../data/fechas_train.csv', "w") as wf:
        wf.write('fecha,fi\n')
        for _ in range(ntrain):
            nmodo = random.randint(0, 1E10)

            if nmodo % 6 == 0:
                fecha, fi = genfecharand()
            elif nmodo % 6 == 1:
                fecha, fi = genfecharandi()
            elif nmodo % 6 == 2:
                fecha, fi = genfecharand2()
            elif nmodo % 6 == 3:
                fecha, fi = genfecharand3()
            elif nmodo % 6 == 4:
                fecha, fi = genfecharand4()
            elif nmodo % 6 == 5:
                fecha, fi = genfecharand5()

            wf.write(f'"{fecha}","{fi}"\n')
            max_length = max(max_length, len(fecha))

    with open('../data/fechas_test.csv', "w") as wf:
        wf.write('fecha,fi\n')
        for _ in range(ntest):
            nmodo = random.randint(0, 1E10)

            if nmodo % 6 == 0:
                fecha, fi = genfecharand()
            elif nmodo % 6 == 1:
                fecha, fi = genfecharandi()
            elif nmodo % 6 == 2:
                fecha, fi = genfecharand2()
            elif nmodo % 6 == 3:
                fecha, fi = genfecharand3()
            elif nmodo % 6 == 4:
                fecha, fi = genfecharand4()
            elif nmodo % 6 == 5:
                fecha, fi = genfecharand5()

            wf.write(f'"{fecha}","{fi}"\n')
            max_length = max(max_length, len(fecha))

    print(f'Maxima longitud caracteres {max_length}')
    print(f'Termino en {round(time.perf_counter() - start, 2)} segundos')
