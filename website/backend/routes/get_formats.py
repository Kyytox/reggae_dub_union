from app import app
from models.models import Vinyl


@app.route("/api/get_all_formats", methods=["GET"])
def get_all_formats():
    """
    Get all vinyl formats from database.

    Returns:
        list: list of vinyl formats
    """

    lst_formats = Vinyl.get_all_formats()

    if not lst_formats:
        return []

    return lst_formats


@app.route("/api/get_formats_by_shop/<int:shop_id>", methods=["GET"])
def get_formats_by_shop(shop_id):
    """
    Get a formats from database by shop id.

    Args:
        shop_id (int): id of the shop

    Returns:
        dict: formats data
    """

    shop = Vinyl.get_formats_by_shop(shop_id)
    print("shop", shop)

    if not shop:
        return {"error": "Shop not found"}, 404

    return shop
