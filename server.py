from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from model import Decade, Country, Book, User, connect_to_db, db

import re
import pickle
import os

from collections import Counter

from textprocessor import make_unique_word_set, unpickle_data


app = Flask(__name__)

app.secret_key = os.environ["FlaskSecretKey"]
app.jinja_env.undefined = StrictUndefined


def compare_single_words(passage, books_from_decade, 
                        words_to_ignore, user_ignore_words):
    '''Find words in user's passage that are not in comparison set of words'''

    words_in_passage = make_unique_word_set(passage)
    comparison_set = set()

    for book in books_from_decade:
        wordset_file = book.word_set
        book_words = unpickle_data(wordset_file)
        comparison_set.update(book_words)

    anachronistic_words = (words_in_passage - user_ignore_words - 
                            words_to_ignore - comparison_set)

    return sorted(list(anachronistic_words))


def format_decades():
    decades = db.session.query(Decade.decade).all()
    return [decade[0] for decade in decades]


def get_ignore_words():
    if not session.get("logged_in"):
        return []
    elif session["logged_in"]==False:
        return []
    else:
        current_user = User.query.filter_by(email=session["user_id"]).one()
        return current_user.ignore_words[:]
        #This is a slice because otherwise SQLAlchemy can't detect changes that we make to the list


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def show_registration():
    return render_template("registration_form.html")


@app.route("/sign-up", methods=["POST"])
def register():
    """Check if user email exists in database and add them as new user if not"""

    email = request.form["email"]
    password = request.form["password"]

    match = User.query.filter_by(email=email).all()

    if not match:
        new_user = User(email=email, password=password, ignore_words=[])
        db.session.add(new_user)
        db.session.commit()

        session["logged_in"] = True
        session["user_id"] = email
        return redirect("/user-page")

    else:
        flash(f"The email address {email} already exists in our database. Please log in here.")
        return redirect("/login")


@app.route("/login")
def show_login_form():
    return render_template("login_form.html")


@app.route("/logout")
def log_out():
    session["logged_in"] = False 
    flash("Logout confirmed.")
    return redirect("/")
    

@app.route("/login-process", methods=["POST"])
def validate_login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user == None:
        flash("Username not found in our system. Please sign up here.")
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
    ignore_words = sorted(get_ignore_words())
    return render_template("user_page.html", ignore_words=ignore_words)


@app.route("/word-search")
def search_for_words():

    return render_template("word_search.html", decades=format_decades())


@app.route("/bigram-search")
def search_for_bigrams():
    return render_template("bigram_search.html", decades=format_decades())


@app.route("/faqs")
def show_faqs():
    return render_template("faqs.html")


@app.route("/corpus")
def show_corpus():
    books = db.session.query(Book.title, Book.author, Book.country, 
        Book.pub_year).order_by(Book.pub_year).all()
    return render_template("our_corpus.html", books=books)


@app.route("/add-ignore-words", methods=["POST"])
def add_ignore_words():

    new_ignore_words = make_unique_word_set(request.form["to-ignore"])
    current_ignore_words = get_ignore_words()

    for word in new_ignore_words:
        current_ignore_words.append(word)

    current_user = User.query.filter_by(email=session["user_id"]).one()
    current_user.ignore_words = current_ignore_words
    db.session.commit()

    return redirect("/user-page")


@app.route("/delete-ignore-words", methods=["POST"])
def delete_ignore_words():

    words_to_remove = set(request.form.getlist("ignore-word"))
    current_ignore_words = set(get_ignore_words())

    current_ignore_words -= words_to_remove

    current_user = User.query.filter_by(email=session["user_id"]).one()
    current_user.ignore_words = list(current_ignore_words)
    db.session.commit()

    return redirect("/user-page")


@app.route("/word-results")
def analyze_words():
    '''Compare user input to set of words from chosen decade & return anachronistic words.'''

    textstring = request.args["textstring"]

    if textstring == "":
        flash("REDIRECT: Input cannot be empty")
        return redirect("/word-search")

    words_to_ignore = make_unique_word_set(request.args["ignore"])

    if session.get("logged_in") == True:
        user_ignore_words = set(get_ignore_words())
    else:
        user_ignore_words = set()

    if len(textstring) > 10000:
        #10000 = 4 times 2500, the length limit on the text box in the HTML form.
        #Textstring becomes > 2500 chars due to HTML encoding but is unlikely to
        #ever expand to 4 times its size, hence 10000-char limit on URL.

        flash("REDIRECT: Input too long")
        return redirect("/word-search")

    decade = request.args["decade"]
    books_from_decade = Book.query.filter_by(decade=decade).all()
    if books_from_decade == []:
        flash(f"{decade} is not a valid decade input")
        return redirect("/word-search")

    anachronistic_words = compare_single_words(textstring, books_from_decade, 
                                words_to_ignore, user_ignore_words)

    return render_template("word_results.html", anachronistic_words=anachronistic_words, 
                            decade=decade)


@app.route("/bigram-results")
def analyze_bigram():

    bigram = request.args["bigram"]

    if len(bigram) > 100:
        flash("Redirect: Input too long")
        return redirect("/bigram-search")

    bigram = bigram.split()

    #Check if bigram input contains exactly 2 words
    if len(bigram) > 2:
        flash("REDIRECT: Bigrams must contain exactly 2 words")
        return redirect("/bigram-search")
    
    try:
        bigram = (bigram[0], bigram[1])
    except IndexError:
        flash("REDIRECT: Bigrams must contain exactly 2 words")
        return redirect("/bigram-search")

    decade = request.args["decade"]
    books_from_decade = Book.query.filter_by(decade=decade).all()
    if books_from_decade == []:
        flash(f"{decade} is not a valid decade input")
        return redirect("/bigram-search")

    comparison_dict = Counter({})

    for book in books_from_decade:
        dict_file = book.bigram_dict
        book_bigrams = Counter(unpickle_data(dict_file))
        comparison_dict += book_bigrams

    corpus_unique_bigrams = "{:,}".format(len(comparison_dict))
    corpus_total = "{:,}".format(sum(comparison_dict.values()))

    corpus_appearances = comparison_dict.get(bigram, 0)
    #Will set corpus_appearances to 0 if bigram not in dictionary

    if corpus_appearances != 0:
        return render_template("bigram_results.html", decade=decade, 
        corpus_appearances=corpus_appearances, corpus_total=corpus_total, 
        bigram=bigram, corpus_unique_bigrams=corpus_unique_bigrams)

    else:
        decade_set = set()
        for book in books_from_decade:
            book_words = unpickle_data(book.word_set)
            decade_set.update(book_words)

        word1 = bigram[0].lower()
        word2 = bigram[1].lower()

        hyphen_bigram = f"{word1}-{word2}"
        smashed_bigram = f"{word1}{word2}"

        hyphenated_found = hyphen_bigram in decade_set
        smashed_found = smashed_bigram in decade_set
        word1_found = word1 in decade_set
        word2_found = word2 in decade_set

        return render_template("bigram_results.html", decade=decade, bigram=bigram,
            hyphenated_found=hyphenated_found, smashed_found=smashed_found, 
            word1_found=word1_found, word2_found = word2_found, word1=word1, 
            word2=word2, hyphen_bigram=hyphen_bigram, smashed_bigram=smashed_bigram,
            corpus_appearances=0)


if __name__ == "__main__":

    connect_to_db(app)
    app.run(port=5000, host="0.0.0.0")