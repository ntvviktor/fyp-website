from .. import db
import datetime
import shortuuid


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))  # decimal
    author = db.Column(db.String(255))
    rating = db.Column(db.String(5))
    description = db.Column(db.Text)
    genre = db.Column(db.String(255))
    image = db.Column(db.String(255))
    datetime = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f'<Product {self.name}>'


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(45))

    def __repr__(self):
        return f'<Genre {self.type}>'
