from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Decade, Country, Book, connect_to_db, db

import re
import pickle

app = Flask(__name__)

app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


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


def unpickle_data(filename):
    infile = open(filename, 'rb')
    unpacked = pickle.load(infile)
    infile.close()
    return unpacked


@app.route('/')
def index():
    """Homepage."""
    decades = db.session.query(Decade.decade).all()

     #Is there a less clunky way to write this?
     #try a list comprehension just to be shorter

    formatted_decades = []
    for decade in decades:
        formatted = decade[0]
        formatted_decades.append(formatted)

    return render_template("index.html", decades=formatted_decades)


# @app.route('/results')
# def see_results():
#     return render_template("results.html", anachronistic_words=anachronistic_words, decade=decade)


@app.route('/process-text')
def analyze_text():
    textstring = remove_irrelevant_characters(request.args["textstring"])
    decade = request.args["decade"]
    books_from_decade = Book.query.filter_by(decade=decade).all()

    if books_from_decade == []:
        return render_template("no-corpus.html", decade=decade)

    else:
            
        if request.args["analysis-type"] == "words":
            word_set = make_unique_word_set(textstring)

            comparison_set = set()

            for book in books_from_decade:
                wordset_file = book.word_set
                book_words = unpickle_data(wordset_file)
                comparison_set.update(book_words)

            anachronistic_words = word_set - comparison_set
            anachronistic_words = sorted(list(anachronistic_words))
            return render_template("results.html", anachronistic_words=anachronistic_words, decade=decade)

        else:
            pass

        return redirect("/results")


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')