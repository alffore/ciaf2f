import torchtext.vocab as vocab
import collections as col

c = col.Counter({'enero': 4, '01': 3, '08': 5, '2021': 4, 'january': 43})

v = vocab.Vocab(c, min_freq=3)

print(v.itos)
print(dict(v.stoi))
