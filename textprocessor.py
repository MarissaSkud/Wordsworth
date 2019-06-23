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


def unpickle_data(filename):
    '''Unpickle a file of a book's word data.'''

    infile = open(filename, "rb")
    unpacked = pickle.load(infile)
    infile.close()
    return unpacked
    

def remove_irrelevant_characters(textstring):
    '''Regular expressions to remove punctuation from string'''
    
    textstring = re.sub("\’", "'", textstring)
    textstring = re.sub("'\W|'$|--|—|\.\.\.", " ", textstring)
    return re.sub("\.|\?|\!|…|,|;|\*|_|\"|\(|\)|:|\”|\“|\‘|\[|\]", "", textstring)


def make_unique_word_set(textstring):
    '''Remove all punctuation & capitalization from string and return set of unique words.'''

    textstring = remove_irrelevant_characters(textstring)
    textstring = textstring.lower()
    split_string = textstring.split()

    return set(split_string)


def make_bigrams(textstring):
    '''Use NLTK to divide text into bigrams'''

    textstring = re.sub('_', "", textstring)
    textstring = re.sub("—|–", "--", textstring)
    text_tokens = nltk.word_tokenize(textstring)
    return list(nltk.bigrams(text_tokens))


def make_bigram_freq_dict(text_bigrams):
    '''Create punctuation-aware dictionary of bigrams and their frequencies'''

    bigram_frequencies = {}

    for bigram in text_bigrams:
        #Ignore bigrams with word(s) that begin with non-alphanumeric characters
        if not bigram[0][0].isalpha() or not bigram[1][0].isalpha():
            pass
        else:
            if bigram in bigram_frequencies:
                bigram_frequencies[bigram] += 1
            else:
                bigram_frequencies[bigram] = 1

    return bigram_frequencies


def prepare_texts(startrange, endrange):
    for i in range(startrange, endrange):
        text = open_and_read_file(f"full_texts/book{i}_full.txt")
        pickle_data(f"word_sets/book{i}_set.pickle", make_unique_word_set(text))
        print(f"Made set for book {i}")
        # pickle_data(f"bigram_dicts/book{i}_dict.pickle", make_bigram_freq_dict(make_bigrams(text)))
        # print(f"Made dict for book {i}")


if __name__ == "__main__":
    prepare_texts(1, 44)
