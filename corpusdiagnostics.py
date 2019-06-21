from server import app, format_decades
from model import Decade, Country, Book, connect_to_db, db

from textprocessor import unpickle_data

def measure_decade_sets():
    with app.app_context():
        decades = format_decades()
        for decade in decades:
            books_from_decade = Book.query.filter_by(decade=decade).all()
            num_books_from_decade = len(books_from_decade)
            decade_set = set()

            for book in books_from_decade:
                decade_set.update(unpickle_data(book.word_set))

            words_from_decade = len(decade_set)
            print(f"The {decade} corpus contains {num_books_from_decade} books and {words_from_decade} unique words")

if __name__ == "__main__":
    connect_to_db(app)
    measure_decade_sets()