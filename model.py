from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Decade(db.Model):
    '''Decade class for data integrity purposes.'''

    __tablename__ = "Decades"

    decade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    decade = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"<Decade {self.decade}, id={self.decade_id}>"


class Country(db.Model):
    '''Country class for data integrity purposes.'''

    __tablename__ = "Countries"

    country_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Country {self.country}, id={self.country_id}>"


class Book(db.Model):
    '''Book class.'''

    __tablename__ = "Books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    pub_year = db.Column(db.Integer, nullable=False)
    ckey = db.Column(db.Integer, db.ForeignKey('Countries.country_id'), nullable=False)
    dkey = db.Column(db.Integer, db.ForeignKey('Decades.decade_id'), nullable=False)
    word_set = db.Column(db.String, nullable=False)
    bigram_dict = db.Column(db.String, nullable=False)


    decade = db.relationship("Decade", backref="books")
    country = db.relationship("Country", backref="books")

    def __repr__(self):
        return f"<Book id={self.book_id}, title={self.title}, published={self.pub_year}>"


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


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

    init_app()
