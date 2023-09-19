import os

from .app import app
from . import db
from .models import Shop, Vinyl, Song


@app.route("/get_vinyls_songs", methods=["GET"])
def get_vinyls_songs():
    """
    Get all vinyls and songs from database.

    Returns:
        list: list of vinyls and songs
    """
    return Vinyl.get_vinyls_and_songs()


@app.route("/get_shops", methods=["GET"])
def get_shops():
    """
    Get all shops from database.

    Returns:
        list: list of shops
    """
    return Shop.get_all_shops()
