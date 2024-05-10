import uuid
from datetime import datetime
from flask_login import UserMixin
from .. import bcrypt, db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(250), primary_key=True)
    username = db.Column(db.String(250))
    full_name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, index=True, unique=True)

    def __init__(self, full_name, username, email, password, is_admin=False, user_id=None):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.is_admin = is_admin
        self.id = user_id if user_id is not None else str(uuid.uuid4())
        self.user_id = self.generate_user_id()

    def generate_user_id(self):
        max_id = db.session.query(db.func.max(User.user_id)).scalar()
        return max_id + 1 if max_id is not None else 1

    def __repr__(self):
        return f"<email {self.email}>"
