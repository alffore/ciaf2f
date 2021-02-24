import torch
import time

from os import path

import dataset as ds
import encoder as enc
import attdecoder as dec

import evaluador

NOM_ARCH_ENCODER = '../modelo/encoder.pth.tar'
NOM_ARCH_ATTDECODER = '../modelo/attdecoder.pth.tar'


MAX_LENGTH = 28
SOS_token = 0
EOS_token = 1

hidden_size = 256

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == '__main__':
    start = time.perf_counter()

    print('Recupera vocabulario ...')
    vocabulario = ds.recuperaVocabP()

    print('Construye modelo ...')
    encoder1 = enc.EncoderRNN(len(vocabulario.itos), hidden_size).to(device)

    attn_decoder1 = dec.AttnDecoderRNN(hidden_size, len(vocabulario.itos)).to(device)

    if path.exists(NOM_ARCH_ENCODER):
        checkpoint = torch.load(NOM_ARCH_ENCODER)
        encoder1.load_state_dict(checkpoint['state_dict'])

    if path.exists(NOM_ARCH_ATTDECODER):
        checkpoint = torch.load(NOM_ARCH_ATTDECODER)
        attn_decoder1.load_state_dict(checkpoint['state_dict'])

    encoder1.eval()
    attn_decoder1.eval()

    print('Estamos listos ...')
    while True:
        fecha = input('Fecha: ')
        if fecha is None or fecha == '' or fecha == 'q':
            break

        output_words, attentions = evaluador.evaluate(encoder1, attn_decoder1, fecha.lower(), vocabulario)
        output_sentence = ''.join(output_words)

        print(f'{fecha} => {output_sentence}')

    print(f'Termino en {round(time.perf_counter() - start, 2)} segundos')
