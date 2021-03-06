
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

matplotlib.use('TkAgg')


def showPlot(points):
    plt.figure()
    fig, ax = plt.subplots()
    # this locator puts ticks at regular intervals
    loc = ticker.MultipleLocator(base=0.2)
    ax.yaxis.set_major_locator(loc)
    plt.plot(points)


def showAttention(input_sentence, output_words, attentions):
    """

    :param input_sentence:
    :param output_words:
    :param attentions:
    :return:
    """
    # Set up figure with colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(attentions.numpy(), cmap='bone')
    fig.colorbar(cax)

    # Set up axes
    # ax.set_xticklabels([''] + input_sentence.split(' ') + ['<EOS>'], rotation=90)
    lcars = []
    for i in range(len(input_sentence)):
        lcars.append(input_sentence[i])
    ax.set_xticklabels([''] + lcars + ['  <EOS>'])
    ax.set_yticklabels([''] + output_words)

    # Show label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.show()
