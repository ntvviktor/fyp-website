from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
import os

es = Elasticsearch("https://localhost:9200",
                   basic_auth=("elastic", "pWO7bI57CVUt9azKZ4ZQ"),
                   verify_certs=False)
print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder='./templates')

    # Configure app, e.g., secret key, database URI
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .views.home import home_bp
    from .views.accounts import accounts_bp
    from .views.admin import admin_bp
    from .views.search import search_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(search_bp)

    from .models.user_model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == str(user_id)).first()

    # Optional: Configure logging, error handlers, etc.

    return app
