import re
import pickle

from server import (make_unique_word_set, remove_irrelevant_characters, 
    make_bigrams_and_frequencies, unpickle_data)

def open_and_read_file(file_path):

    with open(file_path) as data_file:
        return data_file.read()


def pickle_data(filename, dataset):
    outfile = open(filename, "wb")
    pickle.dump(dataset, outfile)
    outfile.close()

text = remove_irrelevant_characters(open_and_read_file("full_texts/book10_full.txt"))

pickle_data("word_sets/book10_set.pickle", make_unique_word_set(text))
pickle_data("bigram_dicts/book10_dict.pickle", make_bigrams_and_frequencies(text))
