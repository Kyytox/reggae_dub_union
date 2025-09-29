import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

load_dotenv()

# create Logger
logger = logging.getLogger("reg_dub_union_backend_logs")
logger.setLevel(logging.INFO)

# create formatter
log_file_name = "reg_dub_union_backend.log"
file_handler = RotatingFileHandler(
    log_file_name,
    maxBytes=1024 * 1024 * 20,  # 20 MB
    backupCount=5,  # keep 5 old log files
)

formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Deactivate Flask's default logger to avoid duplicate logs
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.ERROR)


def create_app():
    """
    Create and configure an instance of the Flask application.

    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from environment
    app.config["FLASK_ENV"] = os.environ.get("FLASK_ENV")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

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
