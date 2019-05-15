import re
import pickle

def open_and_read_file(file_path):

    with open(file_path) as data_file:
        return data_file.read()


def remove_irrelevant_characters(text_string):
    '''Removes commas, colons, semicolons, parentheses, double quotes, underscores, and
    asterisks from text. Replaces long dashes with a single space.'''

    text_string = re.sub(",|;|\*|_|\"|\(|\)|:|\”|\“", "", text_string)
    return text_string.replace("--", " ")


def make_unique_word_set(text_string):
    '''Removes all other punctuation and capitalization from string and returns set of unique words.'''

    text_string = re.sub("\.|\?|\!", "", text_string)
    text_string = text_string.lower()
    split_string = text_string.split()

    word_set = set(split_string)

    return word_set


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


def unpickle_data(filename):
    infile = open(filename, 'rb')
    unpacked = pickle.load(infile)
    infile.close()
    return unpacked

text = remove_irrelevant_characters(open_and_read_file("full_texts/book3_full.txt"))

pickle_data('word_sets/book3_set.pickle', make_unique_word_set(text))
pickle_data('bigram_dicts/book3_dict.pickle', make_bigrams_and_frequencies(text))
