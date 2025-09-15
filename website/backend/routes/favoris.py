from flask import request
from app import app
from models.models import Favori
from routes.auth_utils import decode_auth_token
from utils.libs import format_return_data


def parse_request(request):
    """
    Parse the request data.
    Get the token from the request headers and decode it.

    Args:
        request (Request): The request object.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    # decode token
    token = request.headers.get("Authorization")
    token = token.split(" ")[1]
    topAuth = decode_auth_token(token)

    return topAuth


@app.route("/api/get_list_favoris/<id_user>", methods=["GET"])
def get_list_favoris(id_user):
    """
    Get all favoris from database for a user only with a favoirs table

    Returns:
        list: list of favoris
    """

    # Parse request
    topAuth = parse_request(request)

    # Check if token is valid
    if not topAuth:
        return {"error": "Token is not valid"}

    lst_favoris = Favori.query.filter_by(user_id=id_user).all()

    if len(lst_favoris) == 0:
        return []

    data = []
    for favori in lst_favoris:
        data.append(
            {
                "favori_id": favori.favori_id,
                "vinyl_id": favori.vinyl_id,
                "user_id": favori.user_id,
            }
        )

    return data


@app.route("/api/get_favoris/<id_user>", methods=["GET"])
def get_favoris(id_user):
    """
    Get all favoris from database for a user with vinyls and songs.

    Returns:
        list: list of favoris
    """

    # Parse request
    topAuth = parse_request(request)

    # Check if token is valid
    if not topAuth:
        return {"error": "Token is not valid"}

    df = Favori.get_favoris_by_user(id_user)

    if df.empty:
        return []

    data = format_return_data(df)
    return data


@app.route("/api/toggle_favori", methods=["POST"])
def toggle_favori():
    """
    Toogle a favori to database.

    Returns:
        list: list of favoris
    """

    # Parse request
    topAuth = parse_request(request)

    # Check if token is valid
    if not topAuth:
        return {"error": "Token is not valid"}

    body = request.get_json()
    id_vinyl = body["vinyl_id"]
    id_user = body["user_id"]

    # get favoris
    top_favori = Favori.get_favoris_exist(id_user, id_vinyl)

    # if favori exist
    if top_favori:
        # delete favori
        delete_favori = Favori.query.filter_by(favori_id=top_favori.favori_id).first()
        delete_favori.delete()
        return {"vinyl_id": delete_favori.vinyl_id, "message": "delete"}
    else:
        # create favori
        new_favori = Favori(vinyl_id=id_vinyl, user_id=id_user)
        new_favori.save()
        return {"vinyl_id": new_favori.vinyl_id, "message": "create"}
