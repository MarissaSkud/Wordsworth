from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Decade, Country, Book, connect_to_db, db

import re
import pickle

from collections import Counter


app = Flask(__name__)

app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


def remove_irrelevant_characters(textstring):
    '''Removes commas, colons, semicolons, parentheses, double quotes, underscores, and
    asterisks from text. Replaces long dashes with a single space.'''

    textstring = re.sub(",|;|\*|_|\"|\(|\)|:|\”|\“", "", textstring)
    textstring = textstring.replace("—", " ")
    return textstring.replace("--", " ")


def make_unique_word_set(textstring):
    '''Removes all other punctuation and capitalization from string and returns set of unique words.'''

    textstring = re.sub("\.|\?|\!|…", "", textstring)
    textstring = textstring.lower()
    split_string = textstring.split()

    word_set = set(split_string)

    return word_set


def make_bigrams_and_frequencies(textstring):
    '''Returns dictionary of bigrams and their frequencies.'''

    split_string = textstring.split()

    bigram_frequencies = {}

    for i in range(0, (len(split_string)-1)):
        bigram = (split_string[i], split_string[i+1])

        if bigram in bigram_frequencies:
            bigram_frequencies[bigram] += 1
        else:
            bigram_frequencies[bigram] = 1

    return bigram_frequencies


def unpickle_data(filename):
    infile = open(filename, "rb")
    unpacked = pickle.load(infile)
    infile.close()
    return unpacked


def compare_single_words(passage, books_from_decade, words_to_ignore):
    words_in_passage = make_unique_word_set(passage)

    comparison_set = set()

    for book in books_from_decade:
        wordset_file = book.word_set
        book_words = unpickle_data(wordset_file)
        comparison_set.update(book_words)

    anachronistic_words = words_in_passage - words_to_ignore - comparison_set
    return sorted(list(anachronistic_words))


def format_decades():

    decades = db.session.query(Decade.decade).all()
    return [decade[0] for decade in decades]


@app.route('/')
def index():
    """Homepage."""
    return render_template("index.html")


@app.route("/word-search")
def search_for_words():

    return render_template("word_search.html", decades=format_decades())


@app.route("/bigram-search")
def search_for_bigrams():

    return render_template("bigram_search.html", decades=format_decades())


@app.route("/methodology")
def show_methodology():
    return render_template("methodology.html")


@app.route("/corpus")
def show_corpus():
    books = db.session.query(Book.title, Book.country, Book.pub_year).order_by(Book.pub_year).all()
    return render_template("our_corpus.html", books=books)


@app.route('/words-results')
def analyze_words():
    textstring = remove_irrelevant_characters(request.args["textstring"])
    words_to_ignore = make_unique_word_set(remove_irrelevant_characters(request.args["ignore"]))

    decade = request.args["decade"]
    books_from_decade = Book.query.filter_by(decade=decade).all()

    if books_from_decade == []:
        return render_template("no-corpus.html", decade=decade)

    else:

        anachronistic_words = compare_single_words(textstring, books_from_decade, words_to_ignore)

        if anachronistic_words == []:
            return render_template("words_results.html", decade=decade)

        else:
            return render_template("words_results.html", anachronistic_words=anachronistic_words, 
                    decade=decade)


@app.route('/bigram-results')
def analyze_bigram():
    bigram = remove_irrelevant_characters(request.args["bigram"]).split()
    bigram = (bigram[0], bigram[1])
    decade = request.args["decade"]

    books_from_decade = Book.query.filter_by(decade=decade).all()

    if books_from_decade == []:
        return render_template("no-corpus.html", decade=decade)

    else:

        comparison_dict = Counter({})

        for book in books_from_decade:
            dict_file = book.bigram_dict
            book_bigrams = Counter(unpickle_data(dict_file))
            comparison_dict += book_bigrams

        corpus_total = sum(comparison_dict.values())

        corpus_appearances = comparison_dict.get(bigram, 0)

        return render_template("bigrams_results.html", decade=decade, 
            corpus_appearances=corpus_appearances, corpus_total=corpus_total,
            bigram=bigram)



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")