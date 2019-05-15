from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Decade(db.Model):
    '''Decade class for data integrity purposes.'''

    __tablename__ = "Decades"

    decade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    decade = db.Column(db.String(5), nullable=False, unique=True)

    books = db.relationship("Book")

    def __repr__(self):
        return f"<Decade {self.decade}, id={self.decade_id}>"


class Country(db.Model):
    '''Country class for data integrity purposes.'''

    __tablename__ = "Countries"

    country_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(20), nullable=False, unique=True)

    books = db.relationship("Book")

    def __repr__(self):
        return f"<Country {self.country}, id={self.country_id}>"


class Book(db.Model):
    '''Book class.'''

    __tablename__ = "Books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    pub_year = db.Column(db.Integer, nullable=False)
    country = db.Column(db.Integer, db.ForeignKey('Countries.country'), nullable=False)
    decade = db.Column(db.Integer, db.ForeignKey('Decades.decade'), nullable=False)
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
    db.create_all()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB")


