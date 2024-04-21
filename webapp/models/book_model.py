from .. import db
import datetime
import shortuuid
import uuid
from sqlalchemy.dialects.mysql import LONGTEXT


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.String(36), primary_key=True)
    isbn = db.Column(db.String(255))
    title = db.Column(db.String(255))
    price = db.Column(db.String(30))
    author = db.Column(db.String(255))
    img = db.Column(db.String(255))
    description = db.Column(LONGTEXT)
    url = db.Column(LONGTEXT)
    book_id = db.Column(db.Integer)

    def __init__(self, isbn, title, price, author, img, description, url, book_id):
        self.id = str(shortuuid.uuid())
        self.book_id = book_id
        self.isbn = isbn
        self.title = str(title)
        self.price = price
        self.author = str(author)
        self.img = str(img)
        self.description = str(description)
        self.url = str(url)