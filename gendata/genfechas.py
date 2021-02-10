import random
import datetime
import time

lmeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
          'noviembre', 'diciembre']

lmesesi = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
           'december']
a_min=1600
a_max=2500

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

    asep = ['de', 'del', ' ', '-', '/', ':']

    while bgen:
        nmes = random.randint(0, 11)

        mes = lmeses[nmes]
        nmes += 1

        dia = random.randint(1, 31)
        diamod = random.choice([dia, "{:0>2d}".format(dia)])

        anno = random.randint(a_min, a_max)

        sep1 = random.choice(asep)
        sep2 = random.choice(asep)

        fecha = f'{diamod} {sep1} {mes} {sep2} {anno}'

        fecha = mutacadena(fecha)

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
        anno = random.randint(a_min, a_max)

        mes = mutacadena(mes)

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

    lsep = ['-', '/', ' ', "\\"]

    while bgen:
        nmes = random.randint(1, 12)
        dia = random.randint(1, 31)
        anno = random.randint(a_min, a_max)

        nmesf = "{:0>2d}".format(nmes)

        if nformat % 156 == 0:
            nmesf = nmes

        if nformat % 497 == 0:
            diaf = "{:0>2d}".format(dia)
        else:
            diaf = dia

        sep = random.choice(lsep)

        if nformat % 5 == 0:
            fecha = f'{anno}{sep}{nmesf}{sep}{diaf}'
        elif nformat % 5 == 1:
            fecha = f'{diaf}{sep}{nmesf}{sep}{anno}'
        elif nformat % 5 == 2:
            fecha = f'{nmesf}{sep}{diaf}{sep}{anno}'
        elif nformat % 5 == 3:
            fecha = f'{nmesf}{sep}{nmesf}{sep}{anno}'
        else:
            fecha = f'{nmesf}\\{nmesf}\\{anno}'

        diaf = "{:0>2d}".format(dia)
        fi = f'{anno}-{nmesf}-{diaf}'

        if validafecha(fi):
            bgen = False

    return fecha, fi


def genfecharand4():
    bgen = True

    while bgen:
        nmes = random.randint(0, 11)

        mes = lmeses[nmes]
        mesi = lmesesi[nmes]
        mes = random.choice([mes, mesi])

        nmes += 1

        dia = random.randint(1, 31)
        anno = random.randint(a_min, a_max)

        mes = mutacadena(mes)

        fecha = f'{mes} {dia}, {anno}'

        nmesf = "{:0>2d}".format(nmes)
        diaf = "{:0>2d}".format(dia)

        fi = f'{anno}-{nmesf}-{diaf}'

        if validafecha(fi):
            bgen = False

    return fecha, fi


def mutacadena(cadena):
    c = random.randint(1, 1E9)
    aux = []
    if c % 13 == 0:
        posm = random.randint(0, len(cadena) - 1)
        cl = "a1bc(/de2f3gh,i4jk6lm5n7ñop8qr9s.tuvw0xyz )?"
        cm = cl[random.randint(0, len(cl) - 1)]

        for i in range(len(cadena)):
            if i == posm:
                if c % 2 == 0:
                    aux.append(cm)
            else:
                aux.append(cadena[i])

    if len(aux) > 0:
        cadena = ''.join(aux)
    return cadena


if __name__ == '__main__':
    print("Generador de fechas aleatorias")

    ntrain = 500000
    ntest = 200000
    max_length = 0

    start = time.perf_counter()
    with open('../data/fechas_train.csv', "w") as wf:
        wf.write('fecha,fi\n')
        for _ in range(ntrain):
            nmodo = random.randint(0, 1E10)

            if nmodo % 5 == 0:
                fecha, fi = genfecharand()
            elif nmodo % 5 == 1:
                fecha, fi = genfecharandi()
            elif nmodo % 5 == 2:
                fecha, fi = genfecharand2()
            elif nmodo % 5 == 3:
                fecha, fi = genfecharand3()
            else:
                fecha, fi = genfecharand4()

            wf.write(f'"{fecha}","{fi}"\n')
            max_length = max(max_length, len(fecha))

    with open('../data/fechas_test.csv', "w") as wf:
        wf.write('fecha,fi\n')
        for _ in range(ntest):
            nmodo = random.randint(0, 1E10)

            if nmodo % 5 == 0:
                fecha, fi = genfecharand()
            elif nmodo % 5 == 1:
                fecha, fi = genfecharandi()
            elif nmodo % 5 == 2:
                fecha, fi = genfecharand2()
            elif nmodo % 5 == 3:
                fecha, fi = genfecharand3()
            else:
                fecha, fi = genfecharand4()

            wf.write(f'"{fecha}","{fi}"\n')
            max_length = max(max_length, len(fecha))

    print(f'Maxima longitud caracteres {max_length}')
    print(f'Termino en {round(time.perf_counter() - start, 2)} segundos')
