import torch
import torchtext.vocab as vocab
import pandas as pd
import collections as col


def recuperaDatosVocab(archivo_csv):
    datos = pd.read_csv(archivo_csv)

    lista = []
    for index in range(len(datos)):
        d = datos.values[index]
        d = d[0] + d[1]
        for i in range(len(d)):
            lista.append(d[i])

    counter = col.Counter(lista)

    return datos, vocab.Vocab(counter, min_freq=1)


def data_process_single(sfecha, vocab):
    """

    :param sfecha:
    :param vocab:
    :return:
    """
    toklist = []
    for i in range(len(sfecha)):
        toklist.append(sfecha[i])

    return torch.tensor([vocab[token] for token in toklist], dtype=torch.long)
    # return torch.cat(tuple(filter(lambda t: t.numel() > 0, data)))


def data_process(pdfechas, vocab):
    """

    :type DataSet: pdfechas:
    :type vocab: object
    """
    lista_in = []
    lista_out = []
    for index in range(len(pdfechas)):
        d = pdfechas.values[index]

        lista_in.append(data_process_single(d[0], vocab))
        lista_out.append(data_process_single(d[1], vocab))

    # data_in = torch.cat(tuple(filter(lambda t: t.numel() > 0, lista_in)))
    # data_out = torch.cat(tuple(filter(lambda t: t.numel() > 0, lista_out)))

    data_in = torch.cat(tuple(lista_in))
    data_out = torch.cat(tuple(lista_out))

    return data_in, data_out
