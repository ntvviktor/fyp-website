from flask import Blueprint, render_template
from flask_login import current_user
from webapp.models.book_model import Product


home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    most_viewed_product_ids = range(1, 9)
    on_sale_product_ids = range(21, 29)

    # Query for most viewed products
    most_viewed_products = Product.query.filter(Product.id.in_(most_viewed_product_ids)).all()

    # Query for on sale products
    on_sale_products = Product.query.filter(Product.id.in_(on_sale_product_ids)).all()
    products = Product.query.all()
    if current_user.is_authenticated:
        return render_template("home.html", is_logged_in=True)
    return render_template("home.html", is_logged_in=False, most_viewed_products=most_viewed_products,
                           on_sale_products=on_sale_products)


@home_bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html")