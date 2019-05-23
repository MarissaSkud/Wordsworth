import re
import pickle

from datetime import datetime

from server import make_unique_word_set, unpickle_data

def open_and_read_file(file_path):

    with open(file_path) as data_file:
        return data_file.read()


def pickle_data(filename, dataset):
    outfile = open(filename, "wb")
    pickle.dump(dataset, outfile)
    outfile.close()


def make_bigram_freq_dict(textstring):
    '''Create punctuation-aware dictionary of bigrams and their frequencies'''

    textstring = re.sub('_|\*|\”|\“|\"', "", textstring)
    textstring = re.sub("--|—", " ", textstring)
    text_tokens = nltk.word_tokenize(textstring)
    text_bigrams = list(nltk.bigrams(text_tokens))

    bigram_frequencies = {}

    for bigram in text_bigrams:
        if not bigram[0].isalpha() or not bigram[1].isalpha():
            text_bigrams.remove(bigram)
        else:
            if bigram in bigram_frequencies:
                bigram_frequencies[bigram] += 1
            else:
                bigram_frequencies[bigram] = 1

    return bigram_frequencies


text = open_and_read_file("full_texts/book2_full.txt")

pickle_data("word_sets/book2_set.pickle", make_unique_word_set(text))
pickle_data("bigram_dicts/book2_dict.pickle", make_bigram_freq_dict(text))
