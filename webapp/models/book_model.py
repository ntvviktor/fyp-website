from sqlalchemy import Text

from .. import db
import shortuuid
from sqlalchemy.dialects.mysql import LONGTEXT


class Book(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))
    author = db.Column(db.String(255))
    img = db.Column(db.String(255))
    description = db.Column(LONGTEXT)
    url = db.Column(LONGTEXT)
    average_rating = db.Column(db.DECIMAL(precision=5, scale=2))
    rating_count = db.Column(db.Integer)
    publication_year = db.Column(db.Integer)
    book_id = db.Column(db.Integer)

    def __init__(self, isbn, title, price, author, img, description, url, average_rating, rating_count,
                 publication_year, book_id):
        self.book_id = book_id
        self.isbn = isbn
        self.title = str(title)
        self.price = price
        self.author = str(author)
        self.img = str(img)
        self.description = str(description)
        self.url = str(url)
        self.average_rating = average_rating
        self.rating_count = rating_count
        self.publication_year = publication_year


class OpentrolleyBook(db.Model):
    __tablename__ = 'opentrolley_books'

    id = db.Column(db.String(36), primary_key=True)
    isbn = db.Column(db.String(255), db.ForeignKey('books.isbn'), unique=True, nullable=False)
    price = db.Column(db.String(30))
    img = db.Column(db.String(255))
    url = db.Column(db.String(255))
    provider = db.Column(db.String(30))

    def __init__(self, isbn, price, img, url, provider):
        self.id = str(shortuuid.uuid())
        self.isbn = isbn
        self.img = img
        self.price = price
        self.url = url
        self.provider = provider


class LazadaBook(db.Model):
    __tablename__ = 'lazada_books'

    id = db.Column(db.String(36), primary_key=True)
    isbn = db.Column(db.String(255), db.ForeignKey('books.isbn'), unique=True, nullable=False)
    price = db.Column(db.String(30))
    img = db.Column(Text)
    url = db.Column(Text)
    provider = db.Column(db.String(30))

    def __init__(self, isbn, price, img, url, provider):
        self.id = str(shortuuid.uuid())
        self.isbn = isbn
        self.img = img
        self.price = price
        self.url = url
        self.provider = provider


class NewArrival(db.Model):
    __tablename__ = 'new_arrivals'

    isbn = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))
    author = db.Column(db.String(255))
    img = db.Column(db.String(255))
    description = db.Column(LONGTEXT)
    url = db.Column(LONGTEXT)
    publication_year = db.Column(db.Integer)

    def __init__(self, isbn, title, price, author, img, description, url,
                 publication_year):
        self.isbn = isbn
        self.title = str(title)
        self.price = price
        self.author = str(author)
        self.img = str(img)
        self.description = str(description)
        self.url = str(url)
        self.publication_year = publication_year
