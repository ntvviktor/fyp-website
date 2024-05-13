import pandas as pd
from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType
from webapp import db
from webapp.models.book_model import Book, OpentrolleyBook, LazadaBook, NewArrival
import torch
from webapp.models.favourite_list import FavouriteList
from webapp.models.rating import Interaction, Rating
from webapp.models.review import Review
from webapp.models.user_model import User
from webapp.recommender.content_based_model import get_recommendations
from webapp.recommender.model import model, item_id_map, original_book_data, user_item_df, user_id_map
from webapp.recommender.utils import inference
from pyspark.ml.recommendation import ALS, ALSModel

home_bp = Blueprint("home", __name__)

spark = SparkSession.builder \
    .appName("Book Recommender") \
    .master("local[*]") \
    .config("spark.driver.memory", "1g") \
    .config("spark.driver.memoryOverhead", "512m") \
    .config("spark.memory.fraction", "0.8") \
    .config("spark.default.parallelism", "200") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()


@home_bp.route("/", methods=["GET"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("home.landing_page"))

    if current_user.is_admin:
        return redirect(url_for("admin.admin"))

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
    new_arrivals = NewArrival.query.order_by(NewArrival.publication_year.desc()).limit(5).all()
    return render_template("components/landing_page.html", new_arrivals=new_arrivals)


@home_bp.route("/about", methods=["GET"])
def about():
    if current_user.is_authenticated:
        is_logged_in = current_user.is_authenticated
        username = current_user.username
        return render_template("about.html", is_logged_in=is_logged_in, username=username)
    return render_template("about.html", is_logged_in=False)


@home_bp.route("/book/<string:isbn>", methods=["GET"])
@login_required
def book(isbn):
    if not current_user.is_authenticated:
        return redirect(url_for("home.landing_page"))

    current_book = Book.query.filter(Book.isbn.in_([isbn])).first()
    if current_book is None:
        return render_template("errors/404.html")

    is_logged_in = True

    db_user_id = current_user.user_id
    user_id = torch.LongTensor([db_user_id])
    total_books = Book.query.count()

    # Million dollars recommender inference =))
    insert_interaction(current_user.id, isbn)

    # ratings = Rating.query.filter_by(user_id=current_user.id).all()
    book_exist_in_rating = Rating.query.filter_by(book_isbn=isbn, user_id=current_user.id).first()
    if book_exist_in_rating:
        rated = True
    else:
        rated = False

    current_user_id_in_df = user_id_map.get(db_user_id, 35)
    try:
        als_model = ALSModel.load(f"users/{current_user.user_id}/model.als")
    except Exception as e:
        print("Error loading the ALS model:", e)
        als_model = None
    recommend_books_als = None
    if als_model is not None:
        mylist = [{"user": current_user_id_in_df}]
        schema = StructType([
            StructField("user", LongType(), True)
        ])

        # Create the DataFrame using the list of dictionaries and the defined schema
        user_df = spark.createDataFrame(mylist, schema=schema)
        user_recs = als_model.recommendForUserSubset(user_df, 20)
        item_df = user_recs.selectExpr("user", "explode(recommendations) as rec")
        items = item_df.select("rec.item", "rec.rating")
        unique_items_list = [row['item'] for row in items.select("item").distinct().collect()]
        print(unique_items_list)
        top_k_books_isbn = original_book_data[original_book_data.book_id.isin(unique_items_list)]["isbn"].tolist()
        recommend_books_als = Book.query.filter(Book.isbn.in_(top_k_books_isbn)).all()

    updated_ratings = [0] * total_books

    # Query all interactions for the user
    interactions = Interaction.query.filter_by(user_id=current_user.id).all()
    # Get all ISBNs the user has interacted with
    interacted_isbns = [interaction.book_isbn for interaction in interactions]

    # Update ratings based on the interactions
    for i in interacted_isbns:
        if i in original_book_data['isbn'].values:
            book_id = original_book_data[original_book_data["isbn"] == i]["book_id"].to_list()
            if book_id:
                book_index = item_id_map.get(book_id[0], None)
                if book_index is not None:
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

    opentrolley_book = OpentrolleyBook.query.filter_by(isbn=current_book.isbn).first()
    lazada_book = LazadaBook.query.filter(LazadaBook.isbn.in_([isbn])).first()

    book_isbn_list = FavouriteList.query.with_entities(FavouriteList.book_isbn).filter_by(user_id=current_user.id)
    fav_list = Book.query.filter(Book.isbn.in_(book_isbn_list)).all()
    total_item = len(fav_list)
    total_price = sum([b.price for b in fav_list])

    reviews = (
        db.session.query(Review, User)
        .join(User, Review.user_id == User.id)
        .filter(Review.book_isbn == isbn)
        .all()
    )
    content_based_isbn_list = get_recommendations(current_book.title, 20)
    if content_based_isbn_list is None or len(content_based_isbn_list) is None:
        content_based_isbn_list = []
    similar_books = Book.query.filter(Book.isbn.in_(content_based_isbn_list)).all()
    return render_template("book_details.html",
                           book=current_book,
                           recommend_books=recommend_books,
                           similar_books=similar_books,
                           opentrolley_book=opentrolley_book,
                           lazada_book=lazada_book,
                           is_logged_in=is_logged_in,
                           total_item=total_item,
                           total_price=total_price, username=current_user.username,
                           reviews=reviews,
                           rated=rated,
                           recommend_books_als=recommend_books_als)


def insert_interaction(user_id, book_isbn):
    new_interaction = Interaction(user_id=user_id, book_isbn=book_isbn)
    db.session.add(new_interaction)
    try:
        db.session.commit()
        print("Data inserted successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")


@home_bp.route("/rates/<string:isbn>", methods=["POST"])
@login_required
def rating_book(isbn):
    rating = request.form["rating"]
    rating = int(rating)
    new_rating = Rating(user_id=current_user.id, book_isbn=isbn, rating=rating)
    db.session.add(new_rating)
    try:
        current_user_id_in_df = user_id_map.get(current_user.user_id, 35)
        db.session.commit()
        print("Data inserted successfully!")
        # Check if the book is already rated by the user
        ratings = get_user_ratings(current_user.id)
        # Update user-item DataFrame only if necessary
        if len(ratings) % 5 == 0:
            # Query all interactions for the user
            # Get all ISBNs the user has interacted with
            interacted_isbns = [rating.book_isbn for rating in ratings]
            rating_values = [rating.rating for rating in ratings]

            # Update ratings based on the interactions
            books_id = []
            for isbn in interacted_isbns:
                if isbn in original_book_data['isbn'].values:
                    book_id = original_book_data[original_book_data["isbn"] == isbn]["book_id"].to_list()
                    if book_id:
                        book_index = item_id_map.get(book_id[0], None)
                        if book_index is not None:
                            books_id.append(book_index)
            new_user_ratings = {
                'user': [current_user_id_in_df] * len(rating_values),
                'item': books_id,
                'rating': rating_values
            }
            temp_df = user_item_df[user_item_df['user'] != current_user_id_in_df]

            updated_user_item_df = pd.concat([temp_df, pd.DataFrame(new_user_ratings)], ignore_index=True)
            updated_user_item_df['user'] = updated_user_item_df['user'].astype(int)
            updated_user_item_df['item'] = updated_user_item_df['item'].astype(int)
            updated_user_item_df['rating'] = updated_user_item_df['rating'].astype(float)

            spark_df = spark.createDataFrame(updated_user_item_df, schema="user INT, item INT, rating FLOAT")
            spark_df = spark_df.repartition(200)

            als = ALS(maxIter=1, regParam=0.01, userCol="user", itemCol="item", ratingCol="rating",
                      coldStartStrategy="drop")
            als_model = als.fit(spark_df)
            als_model.write().overwrite().save(f"users/{current_user.user_id}/model.als")
        return render_template("components/rating_response.html")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    return "<h3 class=\"font-bold text-lg\">Some error, please try again!</h3>"


def get_user_ratings(user_id):
    """Get user ratings from the database."""
    return Rating.query.filter_by(user_id=user_id).all()
