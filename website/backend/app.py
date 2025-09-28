import os
from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate
from flask import Flask
from dotenv import load_dotenv

from flask_cors import CORS


load_dotenv()


def create_app():
    """
    Create and configure an instance of the Flask application.

    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)

    app.config["FLASK_ENV"] = os.environ.get("FLASK_ENV")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Initialize the database and migration
    # migrate = Migrate()
    # migrate.init_app(app, db)

    return app


# Create the Flask application
app = create_app()

# Initialize the database
db = SQLAlchemy(app)

CORS(
    app,
    resources={
        r"/api/*": {"origins": ["https://reggaedubunion.fr", "http://localhost:5173"]}
    },
    supports_credentials=True,
)

from routes import get_vinyls
from routes import auth
from routes import favoris
from routes import search
from routes import get_shops
from routes import get_formats


@app.route("/api/")
def index():
    return "Hello World!"
