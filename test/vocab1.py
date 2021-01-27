# https://www.programcreek.com/python/example/123298/torchtext.vocab.Vocab
# Ejemplo 8


import torchtext.vocab as vocab
import collections as col


def test_vocab_basic():
    c = col.Counter({'hello': 4, 'world': 3, 'ᑌᑎIᑕOᗪᕮ_Tᕮ᙭T': 5, 'freq_too_low': 2})
    v = vocab.Vocab(c, min_freq=3, specials=['<unk>', '<pad>', '<bos>'])

    expected_itos = ['<unk>', '<pad>', '<bos>','ᑌᑎIᑕOᗪᕮ_Tᕮ᙭T', 'hello', 'world']
    expected_stoi = {x: index for index, x in enumerate(expected_itos)}

    print(expected_itos)
    print(expected_stoi)

    print(v.itos)
    print(dict(v.stoi))


test_vocab_basic()
