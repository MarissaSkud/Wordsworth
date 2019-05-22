from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Decade, Country, Book, connect_to_db, db

import re
import pickle

import nltk

from collections import Counter


app = Flask(__name__)

app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


def make_unique_word_set(textstring):
    '''Remove all punctuation & capitalization from string and return set of unique words.'''

    textstring = re.sub("\.|\?|\!|…|,|;|\*|_|\"|\(|\)|:|\”|\“", "", textstring)
    textstring = re.sub("--|—", " ", textstring)
    textstring = textstring.lower()
    split_string = textstring.split()

    word_set = set(split_string)

    return word_set


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


def unpickle_data(filename):
    infile = open(filename, "rb")
    unpacked = pickle.load(infile)
    infile.close()
    return unpacked


def compare_single_words(passage, books_from_decade, words_to_ignore):
    '''Find words in user's passage that are not in comparison set of words'''

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
    textstring = request.args["textstring"]
    words_to_ignore = make_unique_word_set(request.args["ignore"])

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
    bigram = request.args["bigram"].split()
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

        corpus_unique_bigrams = len(comparison_dict)
        corpus_total = sum(comparison_dict.values())

        corpus_appearances = comparison_dict.get(bigram, 0)

        return render_template("bigrams_results.html", decade=decade, 
            corpus_appearances=corpus_appearances, corpus_total=corpus_total,
            bigram=bigram, corpus_unique_bigrams=corpus_unique_bigrams)



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")