from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
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
    total_books = Book.query.count()
    total_users = User.query.count()
    graph = create_plot()
    graph2 = create_plot_2()
    return render_template("admin/admin.html", total_books=total_books,
                           total_users=total_users, plot=graph, plot2=graph2)


@admin_bp.route("/add-book", methods=["GET"])
def add_book():
    return render_template("admin/add_book.html")
