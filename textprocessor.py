import re
import pickle

from datetime import datetime

from server import (make_unique_word_set, make_bigram_freq_dict, unpickle_data)

def open_and_read_file(file_path):

    with open(file_path) as data_file:
        return data_file.read()


def pickle_data(filename, dataset):
    outfile = open(filename, "wb")
    pickle.dump(dataset, outfile)
    outfile.close()


text = open_and_read_file("full_texts/book2_full.txt")

pickle_data("word_sets/book2_set.pickle", make_unique_word_set(text))
pickle_data("bigram_dicts/book2_dict.pickle", make_bigram_freq_dict(text))
