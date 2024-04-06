from .. import db
import datetime
import shortuuid
import uuid


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(45))

    def __repr__(self):
        return f'<Genre {self.type}>'


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.String(), primary_key=True)
    isbn = db.Column(db.String(255))
    title = db.Column(db.String(255))
    price = db.Column(db.Float(10, 2))
    author = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    url = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    datetime = db.Column(db.DateTime, default=datetime.datetime.now())
