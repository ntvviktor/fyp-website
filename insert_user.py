from sqlalchemy import create_engine
from webapp.models.user_model import User
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

user = User(full_name="Mr. Admin", username="admin", email="admin@email.com", password="a$$wordd", is_admin=True)

session.add(user)
session.commit()
