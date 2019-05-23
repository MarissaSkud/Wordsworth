import re
import pickle
import nltk

def open_and_read_file(file_path):
    with open(file_path) as data_file:
        return data_file.read()


def pickle_data(filename, dataset):
    outfile = open(filename, "wb")
    pickle.dump(dataset, outfile)
    outfile.close()


def make_unique_word_set(textstring):
    '''Remove all punctuation & capitalization from string and return set of unique words.'''

    textstring = re.sub("\.|\?|\!|…|,|;|\*|_|\"|\(|\)|:|\”|\“|\‘", "", textstring)
    textstring = re.sub("--|—", " ", textstring)
    textstring = textstring.lower()
    split_string = textstring.split()

    word_set = set(split_string)

    return word_set

    #suggest putting the regexes in their own function for purposes of testing
    #or is there a function to just remove punctuation? (but maybe regex is quicker--more performant)
    #what if there is no input?


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


def prepare_texts():
    for i in range(12, 13):
        text = open_and_read_file(f"full_texts/book{i}_full.txt")
        pickle_data(f"word_sets/book{i}_set.pickle", make_unique_word_set(text))
        pickle_data(f"bigram_dicts/book{i}_dict.pickle", make_bigram_freq_dict(text))

