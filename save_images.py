import io
import os
from pathlib import Path

import requests
from PIL import Image
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from webapp.models.book_model import Book

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
session = sessionmaker(bind=engine)()
books = session.query(Book).all()

isbn_list = []
for book in books:
    # image_content = requests.get(book.img).content
    # image_file = io.BytesIO(image_content)
    # image = Image.open(image_file).convert("RGB")
    # filepath = Path("images", f"{book.isbn}.png")
    # image.save(f"./images/{book.isbn}.png", "PNG")
    isbn_list.append(book.isbn)

# with open("isbn_list.txt", "w") as f:
#     for isbn in isbn_list:
#         f.write(isbn + "\n")

