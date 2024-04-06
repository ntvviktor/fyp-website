from flask import Blueprint, render_template
from flask_login import current_user
from webapp.models.book_model import Book


home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    most_viewed_products = Book.query.limit(10).all()

    # Query for on sale products
    on_sale_products = Book.query.limit(10).all()
    if current_user.is_authenticated:
        return render_template("home.html", is_logged_in=True)
    return render_template("home.html", is_logged_in=False, most_viewed_products=most_viewed_products,
                           on_sale_products=on_sale_products)


@home_bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html")
