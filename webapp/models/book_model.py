from .. import db
import datetime
import shortuuid
import uuid


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.String(36), primary_key=True)
    isbn = db.Column(db.String(255))
    title = db.Column(db.String(255))
    price = db.Column(db.Float(10, 2))
    author = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    url = db.Column(db.String(255))
    genre = db.Column(db.String(255))

    def __init__(self, isbn, title, price, author, publisher, url, genre=""):
        self.id = str(uuid.uuid4())
        self.isbn = isbn
        self.title = str(title)
        self.price = price
        self.author = str(author)
        self.publisher = str(publisher)
        self.url = str(url)
        self.genre = str(genre)
