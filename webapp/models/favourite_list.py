from .. import db
import shortuuid


class FavouriteList(db.Model):
    __tablename__ = 'favourite_list'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_isbn = db.Column(db.Integer, db.ForeignKey('books.isbn'))

    def __init__(self, user_id, book_isbn):
        self.id = shortuuid.uuid()
        self.user_id = user_id
        self.book_isbn = book_isbn
