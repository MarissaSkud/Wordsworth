from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import Decade, Country, Book, User, connect_to_db, db

import re
import pickle

from collections import Counter

from textprocessor import make_unique_word_set, unpickle_data


app = Flask(__name__)

app.secret_key = "P12f79xcearx8f"
app.jinja_env.undefined = StrictUndefined


def compare_single_words(passage, books_from_decade, words_to_ignore, user_ignore_words):
    '''Find words in user's passage that are not in comparison set of words'''

    words_in_passage = make_unique_word_set(passage)

    comparison_set = set()

    for book in books_from_decade:
        wordset_file = book.word_set
        book_words = unpickle_data(wordset_file)
        comparison_set.update(book_words)

    anachronistic_words = words_in_passage - user_ignore_words - words_to_ignore - comparison_set
    return sorted(list(anachronistic_words))


def format_decades():
    decades = db.session.query(Decade.decade).all()
    return [decade[0] for decade in decades]


@app.route('/')
def index():
    """Homepage."""
    return render_template("index.html")


@app.route('/registration-form')
def show_registration():
    return render_template("registration_form.html")


@app.route('/sign-up', methods=["POST"])
def register():
    """Check if user email exists in database and add them as new user if not"""

    email = request.form['email']
    password = request.form['password']

    match = User.query.filter_by(email=email).all()

    if not match:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("registration_submitted.html", status="added",
            email=email)

    else:
        return render_template("registration_submitted.html", status="preexisting", 
        email=email)


@app.route("/login")
def show_login_form():
    return render_template("login_form.html")


@app.route("/logout")
def reset_logged_in():
    session["logged_in"] = False 
    return jsonify("Logout confirmed")
    

@app.route("/login-process", methods=["POST"])
def validate_login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user == None:
        flash("Username not found in our system")
        return redirect("/registration-form")

    elif password == user.password:
        session["logged_in"] = True
        session["user_id"] = email
        return redirect("/user-page")

    else:
        flash("Invalid password")
        return redirect("/login")


@app.route("/user-page")
def show_user_page():
    current_user = User.query.filter_by(email=session["user_id"]).one()
    ignore_words = current_user.ignore_words
    return render_template("user_page.html", ignore_words=ignore_words)


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


@app.route("/ignore-words", methods=["POST"])
def add_ignore_words():

    new_ignore_words = make_unique_word_set(request.form["to-ignore"])
    current_user = User.query.filter_by(email=session["user_id"]).one()
    current_ignore_words = current_user.ignore_words[:]
        #This is a list slice because otherwise SQLAlchemy will not be able to detect
        #the changes that we make to the list

    for word in new_ignore_words:
        print(word)
        current_ignore_words.append(word)
        print(current_ignore_words)

    current_user.ignore_words = current_ignore_words
    db.session.commit()

    return redirect("/user-page")


@app.route('/word-results')
def analyze_words():
    '''Compare user input to set of words from chosen decade & return anachronistic words.'''

    textstring = request.args["textstring"]

    if textstring == "":
        flash("REDIRECT: Input cannot be empty")
        return redirect("/word-search")

    words_to_ignore = make_unique_word_set(request.args["ignore"])

    if session["logged_in"] == True:
        current_user = User.query.filter_by(email=session["user_id"]).one()
        user_ignore_words = set(current_user.ignore_words)
    else:
        user_ignore_words = set()

    if len(textstring) > 10000:
        #10000 = 4 times 2500, the length limit on the text box in the HTML form.
        #Textstring becomes > 2500 chars due to HTML encoding but is unlikely to
        #ever expand to 4 times its size, hence 10000-char limit on URL.

        flash("REDIRECT: Input too long")
        return redirect("/word-search")

    decade = request.args["decade"]
    if not decade.isalnum():
        flash("REDIRECT: Invalid decade input")
        return redirect("/word-search")

    books_from_decade = Book.query.filter_by(decade=decade).all()
    if books_from_decade == []:
        return render_template("no_corpus.html", decade=decade)

    else:
        anachronistic_words = compare_single_words(textstring, books_from_decade, 
                                words_to_ignore, user_ignore_words)
        return render_template("word_results.html", 
                anachronistic_words=anachronistic_words,  decade=decade)

#libraries for logging exceptions & also usage stats. or does Flask have a logfile it's creating?
#needs handling to avoid SQL injection on the decades table
#server-side validation to make sure people can't hack my API

#try Pycharm

@app.route('/bigram-results')
def analyze_bigram():
    bigram = request.args["bigram"].split()

    if bigram == "":
        flash("REDIRECT: Input cannot be empty")
        return redirect("/bigram-search")
    elif len(bigram) > 200:
        flash("REDIRECT: Input too long")
        return redirect("/bigram-search")
    else:
        bigram = (bigram[0], bigram[1])

    decade = request.args["decade"]
    if not decade.isalnum():
        flash("REDIRECT: Invalid decade input")
        return redirect("/bigram-search")

    books_from_decade = Book.query.filter_by(decade=decade).all()

    if books_from_decade == []:
        return render_template("no_corpus.html", decade=decade)

    else:

        comparison_dict = Counter({})

        for book in books_from_decade:
            dict_file = book.bigram_dict
            book_bigrams = Counter(unpickle_data(dict_file))
            comparison_dict += book_bigrams

        corpus_unique_bigrams = "{:,}".format(len(comparison_dict))
        corpus_total = "{:,}".format(sum(comparison_dict.values()))

        corpus_appearances = comparison_dict.get(bigram, 0)
        #Will set corpus_appearances to 0 if bigram not in dictionary

        return render_template("bigram_results.html", decade=decade, 
            corpus_appearances=corpus_appearances, corpus_total=corpus_total,
            bigram=bigram, corpus_unique_bigrams=corpus_unique_bigrams)

#also need some try-excepts or if-elses to make sure that request.args["bigram"] was given and throw error if not (and log it!)
#size of my data -- if it gets really large & I do web scraping or something, good to talk about with employers

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")