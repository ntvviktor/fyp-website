from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user
from webapp.models.book_model import Book
from webapp.models.user_model import User
import torch
import pandas as pd
from webapp.recommender.model import train_matrix, model, item_id_map, original_book_data
from webapp.recommender.utils import inference
import plotly
import plotly.graph_objs as go

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["GET"])
def admin():
    total_books = Book.query.count()
    total_users = User.query.count()
    return render_template("admin/admin.html", total_books=total_books, total_users=total_users)


@admin_bp.route("/add-books", methods=["GET"])
def add_books():
    return render_template("admin/add_book.html")