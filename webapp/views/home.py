from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from webapp.models.book_model import Book, OpentrolleyBook
import torch
import pandas as pd
from webapp.recommender.model import train_matrix, model, item_id_map, original_book_data
from webapp.recommender.utils import inference

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    page = request.args.get("page", default=1, type=int)
    if page == 1 and "page" not in request.args:
        return redirect(url_for("home.home", page=1))

    page = int(request.args.get("page"))
    most_viewed_books = Book.query.limit(350).all()
    most_viewed_books = most_viewed_books[(50 * page - 50): (50 * page)]
    if current_user.is_authenticated:
        return render_template(
            "home.html",
            is_logged_in=True,
            most_viewed_books=most_viewed_books,
            page=page,
        )

    return redirect(url_for("home.landing_page"))


@home_bp.route("/home", methods=["GET"])
def landing_page():
    best_sellers = Book.query.limit(5).all()
    return render_template("components/landing_page.html", best_sellers=best_sellers)


@home_bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@home_bp.route("/book/<string:isbn>", methods=["GET"])
@login_required
def book(isbn):
    if not current_user.is_authenticated:
        return redirect(url_for("home.landing_page"))
    is_logged_in = True
    # TODO: Change temporary user id, and query the total book
    user_id = torch.LongTensor([100])
    updated_ratings = [0] * 979
    book_id = original_book_data[original_book_data["isbn"] == isbn]["book_id"].to_list()
    book_index = item_id_map[book_id[0]]
    updated_ratings[book_index] = 1
    user_ratings_tensor = torch.FloatTensor([updated_ratings])
    recommend_books = inference(
        model,
        user_id=user_id,
        user_ratings_tensor=user_ratings_tensor,
        item_id_map=item_id_map,
        apply_dropout=True,
    )

    recommend_books = Book.query.filter(Book.isbn.in_(recommend_books)).all()
    current_book = Book.query.filter(Book.isbn.in_([isbn])).first()
    opentrolley_book = OpentrolleyBook.query.filter(OpentrolleyBook.isbn.in_([isbn])).first()
    # TODO: handle empty case
    if book is None:
        pass
    return render_template("book_details.html", book=current_book,
                           recommend_books=recommend_books, opentrolley_book=opentrolley_book,
                           is_logged_in=is_logged_in)
