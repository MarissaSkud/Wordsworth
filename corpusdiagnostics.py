from server import app
from model import Decade, Country, Book, connect_to_db, db

from textprocessor import unpickle_data


DECADES = ["1800s", "1810s", "1820s", "1830s", "1840s", "1850s", "1860s",
            "1870s", "1880s", "1890s", "1900s", "1910s", "1920s"]

def measure_decade_sets():
    with app.app_context():
        for decade in DECADES:
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