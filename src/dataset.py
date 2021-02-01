import torch
import os
import pandas as pd
import collections as col


def recuperadatos(archivo_csv):
    datos = pd.read_csv(archivo_csv)

    print(datos.size)
    print(len(datos))
    print(len(datos.columns))

    d = datos.values[0]
    print(d[0], d[1])

    lista = []
    for index in range(len(datos)):
        d = datos.values[index]
        lista.append(d[0])
        lista.append(d[1])

    counter = col.Counter(lista)
    print(counter)
