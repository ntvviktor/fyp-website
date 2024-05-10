import werkzeug
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
import os

load_dotenv()

es_password = os.getenv('ES_PASSWORD')
es_host = os.getenv('ELASTICSEARCH_URL')

es = Elasticsearch("https://es01:9200",
                   basic_auth=("elastic", es_password),
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
    from .views.image import image_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(search_bp)
    app.register_blueprint(image_bp)

    @app.errorhandler(werkzeug.exceptions.HTTPException)
    def internal_error(error):
        if error.code == 500:
            return render_template('errors/500.html'), 500
        elif error.code == 404:
            return render_template('errors/404.html'), 404
        return render_template('errors/500.html'), 401

    from .models.user_model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == str(user_id)).first()

    # Optional: Configure logging, error handlers, etc.

    return app
