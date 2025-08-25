from app import app
from models.models import Shop


@app.route("/get_all_shops", methods=["GET"])
def get_all_shops():
    """
    Get all shops from database.

    Returns:
        list: list of shops
    """

    lst_shops = Shop.get_all_shops()

    if not lst_shops:
        return []

    return lst_shops
