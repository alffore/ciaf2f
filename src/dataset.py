import torch
import torchtext.vocab as vocab
import pandas as pd
import collections as col

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def recuperaVocab(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=',', quotechar='"')
    lista = []

    for index in range(len(datos)):
        d = datos.values[index]
        d = str(d[0]) + str(d[1])

        for i in range(len(d)):
            lista.append(d[i])

    return vocab.Vocab(col.Counter(lista), min_freq=1, specials=('<sos>', '<eos>', '<unk>'))


def recuperaDatosVocab(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=',', quotechar='"')
    # datos = pd.read_csv(archivo_csv)

    lista = []
    pairs = []
    for index in range(len(datos)):
        d = datos.values[index]
        pairs.append([d[0], d[1]])
        d = str(d[0]) + str(d[1])

        for i in range(len(d)):
            lista.append(d[i])

    return pairs, vocab.Vocab(col.Counter(lista), min_freq=1, specials=('<sos>', '<eos>', '<unk>'))


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


def indexFromSentence(vocab, sentence):
    toklist = []
    for i in range(len(str(sentence))):
        toklist.append(sentence[i])
    toklist.append('<eos>')
    return [vocab[token] for token in toklist]


def tensorFromSentence(vocab, sentence):
    return torch.tensor(indexFromSentence(vocab, sentence), dtype=torch.long, device=device).view(-1, 1)


def tensorFromPair(vocab, pair):
    input_tensor = tensorFromSentence(vocab, pair[0])
    out_tensor = tensorFromSentence(vocab, pair[1])
    return input_tensor, out_tensor

