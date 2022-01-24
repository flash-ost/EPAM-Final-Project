from config import Config
from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from os import environ


STATUSES = ('Plan To Watch', 'Watching', 'Completed', 'Dropped')
TYPES = ('movie', 'series')
API_KEY = environ.get("API_KEY")


db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask('project')

    # Initialize Flask-Login
    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message_category = 'danger'

    # Initialize config, Flask-SQLAlchemy and Flask-Migrate
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app = Migrate(app, db)
    app.app_context().push()

    # Create shell context
    from models import models
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': models.User, 'Entry': models.Entry, 'Movie': models.Movie}

    # Register blueprints
    from views import search, auth
    app.register_blueprint(search.bp)
    app.register_blueprint(auth.bp)

    # Register API and routes
    from rest.resources import Entry, User
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api = Api(api_bp)
    api.add_resource(Entry, '/entry')
    api.add_resource(User, '/user')
    app.register_blueprint(api_bp)

    # Enable logging in production mode
    import logging
    import os
    from logging.handlers import RotatingFileHandler
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/mymovielist.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('MyMovieList')

    return app