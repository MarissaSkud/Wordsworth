from sqlalchemy import func

from model import Decade, Country, Book, User, connect_to_db, db
from server import app

def load_decades():
    Decade.query.delete()

    for row in open("sql_data/decades"):
        decade = row.rstrip()
        new_decade = Decade(decade=decade)
        db.session.add(new_decade)

    db.session.commit()


def load_countries():
    Country.query.delete()

    for row in open("sql_data/countries"):
        country = row.rstrip()
        new_country = Country(country=country)
        db.session.add(new_country)

    db.session.commit()


def load_books():
    Book.query.delete()

    for row in open("sql_data/books"):
        row = row.rstrip()
        title, pub_year, country, decade, word_set, bigram_dict = row.split("|")

        new_book = Book(title=title, pub_year=pub_year, country=country, decade=decade,
            word_set=word_set, bigram_dict=bigram_dict)
        db.session.add(new_book)

    db.session.commit()


def load_users():
    User.query.delete()

    for row in open("sql_data/users"):
        row = row.rstrip()
        email, password = row.split("|")

        new_user = User(email=email, password=password)
        db.session.add(new_user)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_decades()
    load_countries()
    load_books()
    load_users()
