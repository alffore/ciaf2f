import dataset as ds
import torchtext.vocab as vocab

datos, v = ds.recuperaDatosVocab('../data/fechas_test.csv')
print(v.itos)
print(dict(v.stoi))

# fechas normales
print(ds.data_process_single('2 de febrero del 2021', v))
# print(ds.data_process_single('2021-02-02', v))

# fecha con problema
print(ds.data_process_single('2 de febrerow del 2021', v))


# procesamos todos los datos

tdata_in, tdata_out = ds.data_process(datos, v)

print(tdata_in)
print(tdata_out)
