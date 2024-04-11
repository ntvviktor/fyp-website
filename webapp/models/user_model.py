import uuid
from datetime import datetime
from flask_login import UserMixin
from .. import bcrypt, db


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(250), primary_key=True)
    username = db.Column(db.String(250))
    full_name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, full_name, username, email, password, is_admin=False):
        self.id = str(uuid.uuid4())
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"
