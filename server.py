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


def compare_single_words(passage, books_from_decade):
    words_in_passage = make_unique_word_set(passage)

    comparison_set = set()

    for book in books_from_decade:
        wordset_file = book.word_set
        book_words = unpickle_data(wordset_file)
        comparison_set.update(book_words)

    anachronistic_words = words_in_passage - comparison_set
    return sorted(list(anachronistic_words))


def compare_bigrams(passage, books_from_decade):
    bigrams_in_passage = make_bigrams_and_frequencies(passage)
    passage_denominator = sum(bigrams_in_passage.values())

    comparison_dict = Counter({})

    for book in books_from_decade:
        dict_file = book.bigram_dict
        book_bigrams = Counter(unpickle_data(dict_file))
        comparison_dict += book_bigrams

    corpus_denominator = sum(comparison_dict.values())

    comparison_results = {}

    for bigram in bigrams_in_passage:
        passage_appearances = bigrams_in_passage[bigram]
        passage_frequency = round((bigrams_in_passage[bigram] / passage_denominator *100), 4)
        corpus_appearances = comparison_dict.get(bigram, 0)
        corpus_frequency = round((corpus_appearances / corpus_denominator * 100), 4)

        try:
            ratio = passage_frequency / corpus_frequency

        except ZeroDivisionError:
            ratio = "Bigram not in corpus"

        comparison_results[bigram] = (passage_appearances, corpus_appearances, 
            passage_frequency, corpus_frequency, ratio)

    return comparison_results


@app.route('/')
def index():
    """Homepage."""
    decades = db.session.query(Decade.decade).all()
    formatted_decades = [decade[0] for decade in decades]

    return render_template("index.html", decades=formatted_decades)


@app.route("/methodology")
def show_methodology():
    return render_template("methodology.html")


@app.route("/corpus")
def show_corpus():
    books = db.session.query(Book.title, Book.country, Book.pub_year).order_by(Book.pub_year).all()
    return render_template("our_corpus.html", books=books)


@app.route('/process-text')
def analyze_text():
    textstring = remove_irrelevant_characters(request.args["textstring"])
    decade = request.args["decade"]
    books_from_decade = Book.query.filter_by(decade=decade).all()

    if books_from_decade == []:
        return render_template("no-corpus.html", decade=decade)

    else:

        if request.args["analysis-type"] == "words":

            anachronistic_words = compare_single_words(textstring, books_from_decade)

            if anachronistic_words == []:
                return render_template("words_results.html", decade=decade)

            else:
                return render_template("words_results.html", anachronistic_words=anachronistic_words, 
                    decade=decade)

        if request.args["analysis-type"] == "bigrams":

            comparison_results = compare_bigrams(textstring, books_from_decade)
            
            return render_template("bigrams_results.html", comparison_results=comparison_results, decade=decade)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")