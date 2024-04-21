from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user
from webapp.models.book_model import Book
import torch
import pandas as pd
from webapp.recommender.model import train_matrix, model, item_id_map, original_book_data
from webapp.recommender.utils import inference

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET", "POST"])
def home():
    page = request.args.get("page", default=1, type=int)
    if page == 1 and "page" not in request.args:
        return redirect(url_for("home.home", page=1))

    page = int(request.args.get("page"))
    most_viewed_products = Book.query.limit(350).all()
    print(len(most_viewed_products))
    most_viewed_products = most_viewed_products[(50 * page - 50) : (50 * page + 1)]
    on_sale_products = Book.query.limit(10).all()
    if current_user.is_authenticated:
        return render_template(
            "home.html",
            is_logged_in=True,
            most_viewed_products=most_viewed_products,
            on_sale_products=on_sale_products,
            page=page,
        )

    return render_template(
        "home.html",
        is_logged_in=False,
        most_viewed_products=most_viewed_products,
        on_sale_products=on_sale_products,
        page=page,
    )


@home_bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@home_bp.route("/admin", methods=["GET"])
def admin():
    return render_template("admin/admin.html")


@home_bp.route("/recommend-product/<string:isbn>", methods=["GET"])
def recommend(isbn):
    "Tempprary user id"
    user_id = torch.LongTensor([100])
    updated_ratings = [0] * 979
    book_id = original_book_data[original_book_data["isbn"] == isbn]["book_id"].to_list()
    book_index = item_id_map[book_id[0]]
    updated_ratings[book_index] = 1
    user_ratings_tensor = torch.FloatTensor([updated_ratings])
    recommend_products = inference(
        model,
        user_id=user_id,
        user_ratings_tensor=user_ratings_tensor,
        item_id_map=item_id_map,
        apply_dropout=True,
    )
    
    recommend_products = Book.query.filter(Book.isbn.in_(recommend_products)).all()

    return render_template("components/product_details.html", recommend_products=recommend_products)