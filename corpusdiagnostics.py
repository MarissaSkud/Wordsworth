from server import app, format_decades
from model import Decade, Country, Book, connect_to_db, db

from textprocessor import unpickle_data

from random import sample
from collections import Counter


def measure_and_sample_corpus(data_type, want_sample):
    with app.app_context():
        decades = format_decades()

        for decade in decades:
            books_from_decade = Book.query.filter_by(decade=decade).all()

            if data_type == "word_set":
                num_books_from_decade = len(books_from_decade)
                decade_set = set()

                for book in books_from_decade:
                    decade_set.update(unpickle_data(book.word_set))

                words_from_decade = len(decade_set)
                print(f"The {decade} corpus contains {words_from_decade} unique words")

                if want_sample == True:
                    decade_sample = sample(decade_set, k=10)
                    print(f"Ten of those words are: {decade_sample}")

            if data_type == "bigram_dict":
                decade_dict = Counter({})

                for book in books_from_decade:
                    book_bigrams = Counter(unpickle_data(book.bigram_dict))
                    decade_dict += book_bigrams

                decade_unique_bigrams = "{:,}".format(len(decade_dict))
                decade_total = "{:,}".format(sum(decade_dict.values()))
                print(f"The {decade} corpus contains {decade_unique_bigrams} unique and {decade_total} total bigrams")

                if want_sample == True:
                    decade_sample = sample(decade_dict.keys(), k=10)
                    print(f"Ten of those bigrams are {decade_sample}")


def print_whole_decade_set(data_type, decade):
    with app.app_context():
        books_from_decade = Book.query.filter_by(decade=decade).all()

        if data_type == "word_set":
            decade_set = set()

            for book in books_from_decade:
                decade_set.update(unpickle_data(book.word_set))

            print(f"The {decade} word set:")
            print(sorted(decade_set))

        if data_type == "bigram_dict":
            decade_dict = Counter({})

            for book in books_from_decade:
                book_bigrams = Counter(unpickle_data(book.bigram_dict))
                decade_dict += book_bigrams

            print(f"The {decade} bigram dictionary:")
            print(decade_dict)
            

if __name__ == "__main__":
    connect_to_db(app)
    measure_and_sample_corpus("word_set", True)
    #measure_and_sample_corpus("bigram_dict", False)
    #print_whole_decade_set("word_set", "1920s")