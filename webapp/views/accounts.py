from flask import Blueprint, flash, render_template, redirect, request, url_for, make_response
from flask_login import login_required, login_user, logout_user, current_user

from .. import bcrypt, db
from webapp.models.user_model import User
from webapp.form import LoginForm, RegisterForm
from ..models.book_model import Book
from ..models.favourite_list import FavouriteList

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("home.home"))
    form = LoginForm(request.form)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home.home"))
        flash("Invalid email and/or password.", "danger")

    return render_template("accounts/login.html", form=form)


@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("home.home"))
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = User(full_name=form.fullname.data, username=form.username.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect(url_for("home.home"))

    return render_template("accounts/register.html", form=form)


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))


@accounts_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    is_logged_in = current_user.is_authenticated
    if is_logged_in:
        return render_template("accounts/user_profile.html", is_logged_in=is_logged_in, user=current_user)


@accounts_bp.route("/update-profile", methods=["GET", "PATCH"])
@login_required
def update_profile():
    is_logged_in = current_user.is_authenticated

    if request.method == "GET" and is_logged_in:
        edit_status = request.args.get("edit") == "true"
        name = request.args.get("name")
        if edit_status:
            return render_template("accounts/edit_form.html", user=current_user, name=name)

        return render_template("accounts/cancel_edit_form.html", user=current_user, name=name)

    if request.method == "PATCH" and is_logged_in:
        name = request.args.get("name")
        email = request.form.get("email")
        full_name = request.form.get("fullname")
        username = request.form.get("username")

        user = User.query.filter_by(id=current_user.id).first()

        email = email if email else user.email
        full_name = full_name if full_name else user.full_name
        username = username if username else user.username

        user.email = email
        user.full_name = full_name
        user.username = username

        db.session.commit()

        user = User.query.filter_by(id=current_user.id).first()
        return render_template("accounts/cancel_edit_form.html", user=user, name=name)


@accounts_bp.route("/favourite-list", methods=["GET"])
@login_required
def favourite_list():
    is_logged_in = current_user.is_authenticated
    if is_logged_in:
        book_isbn_list = FavouriteList.query.with_entities(FavouriteList.book_isbn).filter_by(user_id=current_user.id)
        fav_list = Book.query.filter(Book.isbn.in_(book_isbn_list)).all()
        subtotal = sum(book.price for book in fav_list)
        return render_template("accounts/favourite_list.html",
                               is_logged_in=is_logged_in,
                               favourite_list=fav_list,
                               subtotal_price=subtotal)
    return redirect(url_for("home.login"))


@accounts_bp.route("/add-to-favourite", methods=["POST"])
@login_required
def add_to_favourite():
    is_logged_in = current_user.is_authenticated
    if is_logged_in:
        book_isbn = request.args.get("isbn")
        existing_book_isbn = FavouriteList.query.filter_by(book_isbn=book_isbn).first()
        if existing_book_isbn is not None:
            success = False
            return render_template("accounts/add_to_favourite_response.html", success=success)
        fav_item = FavouriteList(user_id=current_user.id, book_isbn=book_isbn)
        db.session.add(fav_item)
        db.session.commit()
        success = True

        return render_template("accounts/add_to_favourite_response.html", success=success)
    return redirect(url_for("accounts.login"))


@accounts_bp.route("/delete-from-favorite/<string:isbn>", methods=["DELETE"])
@login_required
def delete_from_favourite(isbn):
    is_logged_in = current_user.is_authenticated
    if is_logged_in:
        FavouriteList.query.filter(FavouriteList.book_isbn == isbn).delete()
        db.session.commit()

        book_isbn_list = FavouriteList.query.with_entities(FavouriteList.book_isbn).filter_by(user_id=current_user.id)
        fav_list = Book.query.filter(Book.isbn.in_(book_isbn_list)).all()

        return render_template("accounts/favourite_list_inner.html", favourite_list=fav_list)

    return render_template("errors/400.html")


@accounts_bp.route("/favourite-list-summary", methods=["GET"])
@login_required
def favourite_list_summary():
    is_logged_in = current_user.is_authenticated
    if is_logged_in:
        # Query to fetch the list of ISBNs in the user's favorites.
        book_isbn_list = FavouriteList.query.with_entities(FavouriteList.book_isbn). \
            filter_by(user_id=current_user.id).all()
        isbn_list = [isbn for (isbn,) in book_isbn_list]
        # Query to get all books that are in the favorites list.
        if isbn_list:
            fav_list = Book.query.filter(Book.isbn.in_(isbn_list)).all()
        else:
            fav_list = []

        total_item = len(fav_list)
        total_price = sum(book.price for book in fav_list)

        html_content = render_template("accounts/favourite_list_summary.html",
                                       total_item=total_item, total_price=total_price)
        return html_content
    else:
        return render_template("errors/400.html"), 400
