import csv
import os

import pandas as pd
import torch
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from webapp import db
from webapp.models.book_model import Book, NewArrival
from webapp.models.favourite_list import FavouriteList
from webapp.models.user_model import User
from webapp.recommender.CDAE import CDAE
from webapp.recommender.Evaluator import Evaluator
from webapp.recommender.model import create_plot, create_plot_2, dataset
from webapp.recommender.utils import train_model

admin_bp = Blueprint("admin", __name__)
current_dir = os.path.dirname(__file__)
base_dir = os.path.abspath(os.path.join(current_dir, '..'))


@admin_bp.route("/", methods=["GET"])
@login_required
def admin():
    is_logged_in = current_user.is_authenticated
    is_admin = current_user.is_admin
    if not is_admin:
        return render_template("errors/401.html")
    total_books = Book.query.count()
    total_users = User.query.count()
    total_fav_list = FavouriteList.query.count()
    model_metrics_file_path = os.path.join(base_dir, 'recommender', 'model_metrics.csv')
    model_metrics_df = pd.read_csv(model_metrics_file_path)
    precisions = model_metrics_df['Prec@5'].tolist()
    precision = round(precisions[-1]*100, 2)

    graph = create_plot()
    graph2 = create_plot_2()
    return render_template("admin/admin.html",
                           total_books=total_books,
                           total_users=total_users,
                           total_fav_list=total_fav_list,
                           precision=precision,
                           plot=graph, plot2=graph2,
                           is_logged_in=is_logged_in,
                           username=current_user.username)


@admin_bp.route("/view-users", methods=["GET"])
@login_required
def view_users():
    is_admin = current_user.is_admin
    is_logged_in = current_user.is_authenticated
    if is_admin:
        users = User.query.all()
        return render_template("admin/manage_users.html",
                               users=users,
                               is_logged_in=is_logged_in,
                               username=current_user.username)


@admin_bp.route("/add-user", methods=["GET", "POST"])
@login_required
def add_user():
    is_admin = current_user.is_admin
    if not is_admin:
        return render_template("errors/401.html")

    cancel = True if request.args.get("cancel") == "true" else False
    if cancel is True and request.method == "GET":
        users = User.query.all()
        print(users)
        return render_template("admin/view_users.html",
                               users=users)
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
    return render_template("admin/view_users.html",
                           users=users)


@admin_bp.route("/delete-user/<string:id>", methods=["PATCH"])
@login_required
def delete_user(id):
    if current_user.is_admin:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        users = User.query.all()
        return render_template("admin/view_users.html", users=users)


@admin_bp.route("/config-ml", methods=["GET", "POST"])
@login_required
def config_ml():
    if current_user.is_admin:
        if request.method == "GET" and request.args.get("form") == "true":
            return render_template("admin/ml_config_form.html")
        elif request.method == "GET":
            return render_template("admin/ml_config.html",
                                   is_logged_in=current_user.is_authenticated,
                                   username=current_user.username)

        if request.method == "POST":
            print("We are here")
            hidden_dim = int(request.form.get("hidden_dim")) if request.form.get("hidden_dim") else 50
            corruption_ratio = float(request.form.get("corruption_ratio")) if request.form.get("corruption_ratio") else 0.5
            activation = request.form.get("activation") if request.form.get("activation") else "tanh"
            num_epoch = int(request.form.get("num_epoch")) if request.form.get("num_epoch") else 10
            batch_size = int(request.form.get("batch_size")) if request.form.get("batch_size") else 512
            learning_rate = float(request.form.get("learning_rate")) if request.form.get("learning_rate") else 0.001
            early_stop = True
            top_k = 5

            model = CDAE(
                num_users=dataset.num_users, num_items=dataset.num_items, hidden_dim=hidden_dim,
                corruption_ratio=corruption_ratio, activation=activation
            )

            cdae_file_path = os.path.join(base_dir, 'recommender', 'cdae_recommender.pth')
            model.load_state_dict(torch.load(cdae_file_path))
            model.train()

            eval_pos, eval_target = dataset.eval_data()
            item_popularity = dataset.item_popularity

            evaluator = Evaluator(eval_pos, eval_target, item_popularity, top_k)

            cade_model, loss_recorder, metric_recorder = train_model(
                model,
                dataset,
                evaluator,
                batch_size=batch_size,
                test_batch_size=512,
                learning_rate=learning_rate,
                epochs=num_epoch,
                early_stop=early_stop,
            )

            torch.save(cade_model.state_dict(), cdae_file_path)

            model_loss_file_path = os.path.join(base_dir, 'recommender', 'model_loss.csv')
            with open(model_loss_file_path, 'w', newline='') as f:
                wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                wr.writerow(["epoch", "loss"])  # Write header row
                for epoch, loss in enumerate(loss_recorder):
                    wr.writerow([epoch, loss])

            header = ["epoch", "Prec@5", "Recall@5", "NDCG@5", "Nov@5", "Gini-D"]
            model_metrics_file_path = os.path.join(base_dir, 'recommender', 'model_metrics.csv')

            with open(model_metrics_file_path, 'w', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(header)  # Write header row
                for epoch, metrics in enumerate(metric_recorder):
                    row = [epoch] + [metrics.get(metric, "") for metric in header[1:]]
                    writer.writerow(row)

            return render_template("admin/ml_success.html")


@admin_bp.route("/add-book", methods=["GET", "POST"])
@login_required
def add_book():
    is_logged_in = current_user.is_authenticated
    if current_user.is_admin:
        if request.method == "GET":
            return render_template("admin/add_book.html",
                                   is_logged_in=is_logged_in,
                                   username=current_user.username)
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        price = request.form.get("price")
        author = request.form.get("author")
        description = request.form.get("description")
        url = request.form.get("url")
        img = request.form.get("img")
        publication_year = request.form.get("publication_year")

        new_arrival = NewArrival(isbn=isbn, title=title,
                                 price=price, author=author,
                                 img=img,
                                 description=description,
                                 url=url, publication_year=publication_year)

        db.session.add(new_arrival)
        db.session.commit()

        return render_template("admin/add_book.html")