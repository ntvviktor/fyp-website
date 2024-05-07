from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import LONGTEXT

from .. import db


class Review(db.Model):
    __tablename__ = 'reviews'

    user_id = db.Column(db.String(250), db.ForeignKey('users.id', ondelete='CASCADE'))
    book_isbn = db.Column(db.String(255), db.ForeignKey('books.isbn', ondelete='CASCADE'))
    review = db.Column(LONGTEXT)
    rating = db.Column(db.Integer)
    __table_args__ = (
        PrimaryKeyConstraint(
            user_id,
            book_isbn),
        {})

    cascade = "all, delete"

    def __init__(self, user_id, book_isbn, review, rating):
        self.user_id = user_id
        self.book_isbn = book_isbn
        self.review = review
        self.rating = rating
