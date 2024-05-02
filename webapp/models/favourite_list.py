from sqlalchemy import PrimaryKeyConstraint
from .. import db


class FavouriteList(db.Model):
    __tablename__ = 'favourite_list'

    user_id = db.Column(db.String(250), db.ForeignKey('users.id', ondelete='CASCADE'))
    book_isbn = db.Column(db.String(30), db.ForeignKey('books.isbn', ondelete='CASCADE'))

    __table_args__ = (
        PrimaryKeyConstraint(
            user_id,
            book_isbn),
        {})

    cascade = "all, delete"

    def __init__(self, user_id, book_isbn):
        self.user_id = user_id
        self.book_isbn = book_isbn
