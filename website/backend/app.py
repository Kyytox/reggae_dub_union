from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect, url_for, session

from flask_cors import CORS
from utils.config import config


def create_app(config_mode):
    """
    Create and configure an instance of the Flask application.

    Args:
        config_mode (str): The configuration mode to use.

    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)

    # Initialize the database and migration
    # migrate = Migrate()

    # create and configure the app
    app.config.from_object(config[config_mode])
    # migrate.init_app(app, db)

    return app


app = create_app("development")

db = SQLAlchemy(app)

CORS(
    app,
    origins=["http://localhost:3000", "https://reggaedubunion.fr"],
    supports_credentials=True,
)
# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
# CORS(
# app,
# supports_credentials=True,
# expose_headers="Authorization",
# allow_headers=["Authorization", "Content-Type"],
# )


from routes import get_vinyls
from routes import auth
from routes import favoris
from routes import search
from routes import get_shops
from routes import get_formats


#
@app.route("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)
