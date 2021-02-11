import random
import torch
import pandas as pd
import dataset as ds

import ploter

MAX_LENGTH = 27
SOS_token = 0
EOS_token = 1
hidden_size = 256

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def evaluate(encoder, decoder, sentence, vocabulario, max_length=MAX_LENGTH):
    """

    :param encoder:
    :param decoder:
    :param sentence:
    :param vocabulario:
    :param max_length:
    :return:
    """
    with torch.no_grad():
        input_tensor = ds.tensorFromSentence(vocabulario, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(vocabulario.itos[topi.item()])

            decoder_input = topi.squeeze().detach()

        return decoded_words, decoder_attentions[:di + 1]


def evaluateRandomly(encoder, decoder, pairs, vocabulario, n=10):
    """

    :param encoder:
    :param decoder:
    :param pairs:
    :param vocabulario:
    :param n:
    :return:
    """
    for i in range(n):
        pair = random.choice(pairs)
        print('>', pair[0])
        print('=', pair[1])
        output_words, attentions = evaluate(encoder, decoder, pair[0], vocabulario)
        output_sentence = ''.join(output_words)
        print('<', output_sentence)
        print('')


def evaluateAndShowAttention(input_sentence, vocabulario, encoder, attn_decoder):
    """

    :param input_sentence:
    :param vocabulario:
    :param encoder:
    :param attn_decoder:
    :return:
    """
    output_words, attentions = evaluate(
        encoder, attn_decoder, input_sentence, vocabulario)
    print('input =', input_sentence)
    print('output =', ''.join(output_words))
    ploter.showAttention(input_sentence, output_words, attentions)


def evaluatotal(archivo_csv, encoder, decoder, vocabulario, max_length=MAX_LENGTH):
    """

    :param archivo_csv:
    :param encoder:
    :param decoder:
    :param vocabulario:
    :param max_length:
    :return:
    """
    datos = pd.read_csv(archivo_csv, sep=',', quotechar='"')

    total_entradas = len(datos)
    porexac = 0.0

    with torch.no_grad():
        for index in range(len(datos)):
            d = datos.values[index]
            pair = ds.tensorFromPair(vocabulario, [d[0], d[1]])

            input_tensor = ds.tensorFromSentence(vocabulario, d[0])
            input_length = input_tensor.size()[0]
            encoder_hidden = encoder.initHidden()

            encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

            for ei in range(input_length):
                encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                         encoder_hidden)
                encoder_outputs[ei] += encoder_output[0, 0]

            decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

            decoder_hidden = encoder_hidden

            decoded_words = []
            decoder_attentions = torch.zeros(max_length, max_length)

            lista_topi = []
            for di in range(max_length):
                decoder_output, decoder_hidden, decoder_attention = decoder(
                    decoder_input, decoder_hidden, encoder_outputs)
                decoder_attentions[di] = decoder_attention.data
                topv, topi = decoder_output.data.topk(1)
                lista_topi.append(topi.item())
                if topi.item() == EOS_token:
                    decoded_words.append('<EOS>')
                    break
                else:
                    decoded_words.append(vocabulario.itos[topi.item()])

                decoder_input = topi.squeeze().detach()

            # a = torch.tensor(pair[1].view(-1)).float()
            a = torch.tensor(pair[1].clone().detach().view(-1)).float()
            c = torch.sum(a) - torch.sum(torch.tensor(lista_topi, device=device).float())

            if c == 0.0:
                porexac = porexac + 1

    return porexac * 100.0 / total_entradas
