from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from .config import config

# import SQL Alchemy
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_mode):
    """
    Create and configure an instance of the Flask application.

    Args:
        config_mode (str): The configuration mode to use.

    Returns:
        Flask: The Flask application instance.
    """

    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object(config[config_mode])

    # initialize the app
    db.init_app(app)
    migrate.init_app(app, db)

    return app
