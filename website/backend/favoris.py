import os
import json
import requests

from flask import request
from .app import app
from . import db
from .models import Favori
from .auth_utils import decode_auth_token


@app.route("/get_favoris/<id_user>", methods=["GET"])
def get_favoris(id_user):
    """
    Get all favoris from database for a user.

    Returns:
        list: list of favoris
    """

    # decode token
    token = request.headers.get("Authorization")
    token = token.split(" ")[1]
    topAuth = decode_auth_token(token)

    # if token is not valid
    if topAuth:
        return Favori.get_favoris_by_user(id_user)
    else:
        return "Token is not valid"


@app.route("/toggle_favori", methods=["POST"])
def toggle_favori():
    """
    Toogle a favori to database.

    Returns:
        list: list of favoris
    """

    token = request.headers.get("Authorization")
    token = token.split(" ")[1]
    topAuth = decode_auth_token(token)

    if topAuth:
        body = request.get_json()["body"]
        id_vinyl = body["id_vinyl"]
        id_song = body["id_song"]
        id_user = body["id_user"]

        # get favoris
        top_favori = Favori.get_favoris_exist(id_user, id_vinyl, id_song)

        # if favori exist
        if top_favori:
            # delete favori
            delete_favori = Favori.query.filter_by(id=top_favori.id).first()
            delete_favori.delete()
            return {"song_id": delete_favori.id_song, "message": "delete"}
        else:
            # create favori
            new_favori = Favori(id_vinyl=id_vinyl, id_song=id_song, id_user=id_user)
            new_favori.save()
            return {"song_id": new_favori.id_song, "message": "create"}
    else:
        return "Token is not valid"
