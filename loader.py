from elasticsearch import Elasticsearch
from sqlalchemy import create_engine, select
import webapp.models.book_model as book_model
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
"""
Token:
"""

client = Elasticsearch("https://localhost:9200",
                       basic_auth=("elastic", os.getenv("ES_PASSWORD")), verify_certs=False)

print(f"Connected to the elasticsearch server `{client.info().body['cluster_name']}`")

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

book_obj = session.query(book_model.Book).all()

# Extracting the IDs from the response
# document_ids = [hit["_id"] for hit in response["hits"]["hits"]]

# resp = client.indices.delete(
#     index="books",
# )
# print(resp)

for i, book in enumerate(book_obj):
    document = {
        "title": book.title,
        "author": book.author,
        "year": book.publication_year,
    }
    client.index(index="books", id=book.isbn, document=document)
