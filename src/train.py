from __future__ import unicode_literals, print_function, division

import random
from os import path

import torch
import torch.nn as nn
from torch import optim

import time
import math

import dataset as ds

import encoder as enc
import attdecoder as dec

import evaluador
import ploter

teacher_forcing_ratio = 0.5

MAX_LENGTH = 27
SOS_token = 0
EOS_token = 1

hidden_size = 256

NOM_ARCH_ENCODER = '../modelo/encoder.pth.tar'
NOM_ARCH_ATTDECODER = '../modelo/attdecoder.pth.tar'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion,
          max_length=MAX_LENGTH):
    """

    :param input_tensor:
    :param target_tensor:
    :param encoder:
    :param decoder:
    :param encoder_optimizer:
    :param decoder_optimizer:
    :param criterion:
    :param max_length:
    :return:
    """
    encoder_hidden = encoder.initHidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)
    target_length = target_tensor.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[SOS_token]], device=device)

    decoder_hidden = encoder_hidden

    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

    if use_teacher_forcing:
        # Teacher forcing: Feed the target as the next input
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            loss += criterion(decoder_output, target_tensor[di])
            decoder_input = target_tensor[di]  # Teacher forcing

    else:
        # Without teacher forcing: use its own predictions as the next input
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            topv, topi = decoder_output.topk(1)
            decoder_input = topi.squeeze().detach()  # detach from history as input

            loss += criterion(decoder_output, target_tensor[di])
            if decoder_input.item() == EOS_token:
                break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_length


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))


def trainItersFechas(encoder, decoder, niters, vocabulario, print_every=1000, plot_every=100, learning_rate=0.01):
    """

    :param encoder:
    :param decoder:
    :param niters:
    :param vocabulario:
    :param print_every:
    :param plot_every:
    :param learning_rate:
    :return:
    """
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)

    if path.exists(NOM_ARCH_ENCODER):
        load_checkpoint(NOM_ARCH_ENCODER, encoder, encoder_optimizer)

    if path.exists(NOM_ARCH_ATTDECODER):
        load_checkpoint(NOM_ARCH_ATTDECODER, decoder, decoder_optimizer)

    training_pairs = [ds.tensorFromPair(vocabulario, random.choice(pairs)) for i in range(niters)]
    criterion = nn.NLLLoss()

    print_loss_avg_ant = -1

    for iter in range(1, niters + 1):
        training_pair = training_pairs[iter - 1]
        input_tensor = training_pair[0]
        target_tensor = training_pair[1]
        loss = train(input_tensor, target_tensor, encoder,
                     decoder, encoder_optimizer, decoder_optimizer, criterion)
        print_loss_total += loss
        plot_loss_total += loss

        if iter % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (timeSince(start, iter / niters),
                                         iter, iter / niters * 100, print_loss_avg))
            if print_loss_avg_ant < 0.0:
                print_loss_avg_ant = print_loss_avg

            if print_loss_avg_ant > print_loss_avg:
                print(f'Guarda {(print_loss_avg_ant - print_loss_avg) / print_loss_avg_ant}')
                print_loss_avg_ant = print_loss_avg
                checkpoint_encoder = {"state_dict": encoder.state_dict(), "optimizer": encoder_optimizer.state_dict(), }
                save_checkpoint(checkpoint_encoder, filename=NOM_ARCH_ENCODER)
                checkpoint_decoder = {"state_dict": decoder.state_dict(), "optimizer": decoder_optimizer.state_dict(), }
                save_checkpoint(checkpoint_decoder, filename=NOM_ARCH_ATTDECODER)

        if iter % plot_every == 0:
            plot_loss_avg = plot_loss_total / plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0

    ploter.showPlot(plot_losses)


def save_checkpoint(state, filename="my_checkpoint.pth.tar"):
    print(f'=> Saving checkpoint: {filename}')
    torch.save(state, filename)


def load_checkpoint(filename, model, optimizer):
    print(f"=> Loading checkpoint: {filename}")
    checkpoint = torch.load(filename)
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])


if __name__ == "__main__":
    print("Recupera datos, genera vocabulario")
    pairs, vocabulario = ds.recuperaDatosVocab('../data/fechas_train.csv')

    encoder1 = enc.EncoderRNN(len(vocabulario.itos), hidden_size).to(device)

    attn_decoder1 = dec.AttnDecoderRNN(hidden_size, len(vocabulario.itos), dropout_p=0.1).to(device)

    trainItersFechas(encoder1, attn_decoder1, 100000, vocabulario, print_every=1000)

    print("Evaluación completa")
    evaluador.evaluateRandomly(encoder1, attn_decoder1, pairs, vocabulario)

    evaluador.evaluateAndShowAttention("1 del agosto de 1973", vocabulario, encoder1, attn_decoder1)

    evaluador.evaluateAndShowAttention("1 de agoso del 1973", vocabulario, encoder1, attn_decoder1)

    evaluador.evaluateAndShowAttention("2 de aagosto del 1973", vocabulario, encoder1, attn_decoder1)

    evaluador.evaluateAndShowAttention("2 agosto  del 1973", vocabulario, encoder1, attn_decoder1)

    rese = evaluador.evaluatotal('../data/fechas_test.csv', encoder1, attn_decoder1, vocabulario)
    print(rese)
