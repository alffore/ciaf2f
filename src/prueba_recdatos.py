import dataset as ds
import time
import random

start = time.perf_counter()

pairs, v = ds.recuperadatosvocab('../data/fechas_train.csv')
print(v.itos)
print(f'cantidad de simbolos: {len(v.itos)}')
print(dict(v.stoi))
print(v.freqs)

# fechas normales
print(ds.data_process_single('2 de febrero del 2021', v))

# fecha con problema
print(ds.data_process_single('2 de febrerow del 2021', v))

# fecha convertida
print(ds.data_process_single('2021-02-02', v))

# tensor from pair
print(ds.tensorFromPair(v,['2 de febrerow del 2021', '2021-02-02']))

print('Pares:')
print(random.choice(pairs))

print(f'Termino en {round(time.perf_counter() - start, 2)} segundos')
