import re
import pickle

from server import make_unique_word_set, remove_irrelevant_characters, unpickle_data

def open_and_read_file(file_path):

    with open(file_path) as data_file:
        return data_file.read()

def make_bigrams_and_frequencies(text_string):
    '''Returns dictionary of bigrams and their frequencies.'''

    split_string = text_string.split()

    bigram_frequencies = {}

    for i in range(0, (len(split_string)-1)):
        bigram = (split_string[i], split_string[i+1])

        if bigram in bigram_frequencies:
            bigram_frequencies[bigram] += 1

        else:
            bigram_frequencies[bigram] = 1

    return bigram_frequencies


def pickle_data(filename, dataset):
    outfile = open(filename, 'wb')
    pickle.dump(dataset, outfile)
    outfile.close()

text = remove_irrelevant_characters(open_and_read_file("full_texts/book7_full.txt"))

pickle_data('word_sets/book7_set.pickle', make_unique_word_set(text))
pickle_data('bigram_dicts/book7_dict.pickle', make_bigrams_and_frequencies(text))
