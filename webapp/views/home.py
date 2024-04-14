from flask import Blueprint, render_template
from flask_login import current_user
from webapp.models.book_model import Book
import torch
import pandas as pd
from webapp.recommender.model import train_matrix, model, item_id_map
from webapp.recommender.utils import inference

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    most_viewed_products = Book.query.limit(10).all()

    # Query for on sale products
    on_sale_products = Book.query.limit(10).all()
    if current_user.is_authenticated:
        user_id = torch.LongTensor([500])
        user_ratings_tensor = torch.FloatTensor([train_matrix.toarray()[50]])
        recommend_products = inference(model, user_id=user_id, user_ratings_tensor=user_ratings_tensor,
                                       item_id_map=item_id_map, apply_dropout=True)
        recommend_products = Book.query.filter(Book.isbn.in_(recommend_products)).all()
        return render_template("home.html", is_logged_in=True,
                               recommend_products=recommend_products,
                               on_sale_products=on_sale_products)

    return render_template("home.html", is_logged_in=False, most_viewed_products=most_viewed_products,
                           on_sale_products=on_sale_products)


@home_bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@home_bp.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")