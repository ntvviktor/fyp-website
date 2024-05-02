from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from webapp.models.book_model import Book, OpentrolleyBook, LazadaBook
import torch

from webapp.models.favourite_list import FavouriteList
from webapp.recommender.model import model, item_id_map, original_book_data
from webapp.recommender.utils import inference

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("home.landing_page"))

    page = request.args.get("page")
    sort_by = request.args.get("sort")
    if not page or not page.isdigit():
        return redirect(url_for("home.home", page=1))

    page = int(page)

    if sort_by == "newest":
        books = Book.query.order_by(Book.publication_year.desc()).limit(350).all()
    elif sort_by == "price-asc":
        books = Book.query.order_by(Book.price).limit(350).all()
    elif sort_by == "price-desc":
        books = Book.query.order_by(Book.price.desc()).limit(350).all()
    else:
        books = Book.query.order_by(Book.average_rating.desc()).limit(350).all()

    book_isbn_list = FavouriteList.query.with_entities(FavouriteList.book_isbn).filter_by(user_id=current_user.id)
    fav_list = Book.query.filter(Book.isbn.in_(book_isbn_list)).all()
    total_item = len(fav_list)
    total_price = sum([b.price for b in fav_list])

    books = books[(50 * page - 50): (50 * page)]

    return render_template(
        "home.html",
        is_logged_in=True,
        books=books,
        page=page,
        total_item=total_item,
        total_price=total_price,
        username=current_user.username
    )


@home_bp.route("/home", methods=["GET"])
def landing_page():
    best_sellers = Book.query.limit(5).all()
    return render_template("components/landing_page.html", best_sellers=best_sellers)


@home_bp.route("/about", methods=["GET"])
def about():
    is_logged_in = current_user.is_authenticated
    username = current_user.username
    return render_template("about.html", is_logged_in=is_logged_in, username=username)


@home_bp.route("/book/<string:isbn>", methods=["GET"])
@login_required
def book(isbn):
    if not current_user.is_authenticated:
        return redirect(url_for("home.landing_page"))

    current_book = Book.query.filter(Book.isbn.in_([isbn])).first()
    if current_book is None:
        return render_template("errors/404.html")

    is_logged_in = True
    # TODO: Change temporary user id, and query the total book
    user_id = torch.LongTensor([100])
    total_books = Book.query.count()
    updated_ratings = [0] * total_books
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

    opentrolley_book = OpentrolleyBook.query.filter(OpentrolleyBook.isbn.in_([isbn])).first()
    lazada_book = LazadaBook.query.filter(LazadaBook.isbn.in_([isbn])).first()

    book_isbn_list = FavouriteList.query.with_entities(FavouriteList.book_isbn).filter_by(user_id=current_user.id)
    fav_list = Book.query.filter(Book.isbn.in_(book_isbn_list)).all()
    total_item = len(fav_list)
    total_price = sum([b.price for b in fav_list])
    # TODO: handle empty case

    return render_template("book_details.html", book=current_book,
                           recommend_books=recommend_books,
                           opentrolley_book=opentrolley_book,
                           lazada_book=lazada_book,
                           is_logged_in=is_logged_in,
                           total_item=total_item,
                           total_price=total_price, username=current_user.username)
