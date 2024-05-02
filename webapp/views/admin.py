from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webapp import db
from webapp.models.book_model import Book
from webapp.models.user_model import User
import torch
import pandas as pd
from webapp.recommender.model import train_matrix, model, item_id_map, original_book_data, create_plot, create_plot_2
from webapp.recommender.utils import inference
import plotly
import plotly.graph_objs as go

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["GET"])
@login_required
def admin():
    is_logged_in = current_user.is_authenticated
    is_admin = current_user.is_admin
    if not is_admin:
        return render_template("errors/401.html")
    total_books = Book.query.count()
    total_users = User.query.count()
    graph = create_plot()
    graph2 = create_plot_2()
    return render_template("admin/admin.html", total_books=total_books,
                           total_users=total_users, plot=graph, plot2=graph2, is_logged_in=is_logged_in)


@admin_bp.route("/view-users", methods=["GET"])
@login_required
def view_users():
    is_admin = current_user.is_admin
    is_logged_in = current_user.is_authenticated
    if is_admin:
        users = User.query.all()
        return render_template("admin/manage_users.html",
                               users=users, is_logged_in=is_logged_in)


@admin_bp.route("/add-user", methods=["GET", "POST"])
@login_required
def add_user():
    is_admin = current_user.is_admin
    if not is_admin:
        return render_template("errors/401.html")

    if request.method == "GET":
        return render_template("admin/add_user_form.html")

    full_name = request.form.get("fullname")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    is_admin = True if request.form.get("is_admin") == "1" else False

    user = User(full_name=full_name,
                username=username,
                email=email,
                password=password,
                is_admin=is_admin)
    db.session.add(user)
    db.session.commit()

    users = User.query.all()
    return render_template("admin/view_users.html", users=users)


@admin_bp.route("/delete-user/<string:id>", methods=["PATCH"])
@login_required
def delete_user(id):
    if current_user.is_admin:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        users = User.query.all()
        return render_template("admin/view_users.html", users=users)
