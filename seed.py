from sqlalchemy import func

from model import Decade
from model import Country
from model import Book

from model import connect_to_db, db
from server import app

def load_decades():
    Decade.query.delete()

    for row in open("sql_data/u.decades"):
        decade = row.rstrip()
        new_decade = Decade(decade=decade)
        db.session.add(new_decade)

    db.session.commit()


def load_countries():
    Country.query.delete()

    for row in open("sql_data/u.countries"):
        country = row.rstrip()
        new_country = Country(country=country)
        db.session.add(new_country)

    db.session.commit()


def load_books():
    Book.query.delete()

    for row in open("sql_data/u.books"):
        row = row.rstrip()
        title, pub_year, country, decade, word_set, bigram_dict = row.split("|")

        new_book = Book(title=title, pub_year=pub_year, country=country, decade=decade,
            word_set=word_set, bigram_dict=bigram_dict)
        db.session.add(new_book)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_decades()
    load_countries()
    load_books()
