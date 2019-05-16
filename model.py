from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Decade(db.Model):
    '''Decade class for data integrity purposes.'''

    __tablename__ = "decades"
    decade = db.Column(db.String(5), primary_key=True)

    books = db.relationship("Book")

    def __repr__(self):
        return f"<Decade {self.decade}>"


class Country(db.Model):
    '''Country class for data integrity purposes.'''

    __tablename__ = "countries"

    country = db.Column(db.String(20), primary_key=True)

    books = db.relationship("Book")

    def __repr__(self):
        return f"<Country {self.country}>"


class Book(db.Model):
    '''Book class.'''

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    pub_year = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(20), db.ForeignKey('countries.country'), nullable=False)
    decade = db.Column(db.String(5), db.ForeignKey('decades.decade'), nullable=False)
    word_set = db.Column(db.String, nullable=False)
    bigram_dict = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Book id={self.book_id}, title={self.title}, published={self.pub_year}>"


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///source_texts'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB")


