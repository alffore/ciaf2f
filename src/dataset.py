import torch
import torchtext.vocab as vocab
import pandas as pd
import collections as col
import pickle
from os import path

NOM_ARCH_VOC = "../modelo/voccol.pkl"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def recuperaVocabP(archivo_csv='../data/fechas_train.csv'):
    """

    :param archivo_csv:
    :return:
    """
    if path.exists(NOM_ARCH_VOC):
        with open(NOM_ARCH_VOC, "rb") as file:
            coleccion = pickle.load(file)
            # return vocab.Vocab(coleccion, min_freq=1, specials=('<sos>', '<eos>', '<unk>'))
            return vocab.build_vocab_from_iterator(coleccion, min_freq=1, specials=('<sos>', '<eos>', '<unk>'))

    return recuperaVocab(archivo_csv)


def recuperaVocab(archivo_csv):
    """
    Genera el puro vocabulario
    :param archivo_csv:
    :return:
    """
    datos = pd.read_csv(archivo_csv, sep=',', quotechar='"')
    lista = []

    for index in range(len(datos)):
        d = datos.values[index]
        d = str(d[0]) + str(d[1])

        for i in range(len(d)):
            lista.append(d[i])

    coleccion = col.Counter(lista)

    with open(NOM_ARCH_VOC, "wb") as file:
        pickle.dump(coleccion, file)

    return vocab.Vocab(coleccion, min_freq=1, specials=('<sos>', '<eos>', '<unk>'))


def recuperadatosvocab(archivo_csv):
    """
    Recupera datos y vocabulario
    :param archivo_csv:
    :return:
    """
    datos = pd.read_csv(archivo_csv, sep=',', quotechar='"')

    lista = []
    pairs = []
    for index in range(len(datos)):
        d = datos.values[index]
        pairs.append([d[0], d[1]])
        d = str(d[0]) + str(d[1])

        for i in range(len(d)):
            lista.append(d[i])

    coleccion = col.Counter(lista)
    with open(NOM_ARCH_VOC, "wb") as file:
        pickle.dump(coleccion, file)

    # return pairs, vocab.Vocab(coleccion, min_freq=1, specials=('<sos>', '<eos>', '<unk>'))
    return pairs, vocab.build_vocab_from_iterator(coleccion, min_freq=1, specials=('<sos>', '<eos>', '<unk>'))


def data_process_single(sfecha, vocab):
    """

    :param sfecha:
    :param vocab:
    :return:
    """
    toklist = []
    for i in range(len(str(sfecha))):
        toklist.append(sfecha[i])
    toklist.append('<eos>')

    return torch.tensor([vocab[token] for token in toklist], dtype=torch.long)


def indexFromSentence(vocabulario, sentence):
    toklist = []
    for i in range(len(str(sentence))):
        toklist.append(sentence[i])
    toklist.append('<eos>')
    dic = vocabulario.get_stoi()
    return [dic[token] for token in toklist]


def tensorFromSentence(vocabulario, sentence):
    return torch.tensor(indexFromSentence(vocabulario, sentence), dtype=torch.long, device=device).view(-1, 1)


def tensorFromPair(vocabulario, pair):
    input_tensor = tensorFromSentence(vocabulario, pair[0])
    out_tensor = tensorFromSentence(vocabulario, pair[1])
    return input_tensor, out_tensor
