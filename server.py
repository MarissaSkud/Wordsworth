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


@app.route('/')
def index():
    """Homepage."""
    decades = db.session.query(Decade.decade).all()

     #Is there a less clunky way to write this?

    formatted_decades = []
    for decade in decades:
        formatted = decade[0]
        formatted_decades.append(formatted)

    return render_template("index.html", decades=formatted_decades)


@app.route('/results')
def see_results():
    return render_template("results.html")


@app.route('/process-text')
def analyzer():
    textstring = remove_irrelevant_characters(request.args["textstring"])
    print(textstring)

    if request.args["analysis-type"] == "words":
        pass

    return redirect("/results")


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')