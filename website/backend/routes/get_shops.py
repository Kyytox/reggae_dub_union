from app import app
from models.models import Shop


@app.route("/api/get_all_shops", methods=["GET"])
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


@app.route("/get_shop_by_id/<int:shop_id>", methods=["GET"])
def get_shop_by_id(shop_id):
    """
    Get a shop from database by id.

    Args:
        shop_id (int): id of the shop

    Returns:
        dict: shop data
    """

    print("shop_id", shop_id)
    shop = Shop.get_shop_by_id(shop_id)
    print("shop", shop)

    if not shop:
        return {"error": "Shop not found"}, 404

    return shop


@app.route("/get_shops_by_format/<string:vinyl_format>", methods=["GET"])
def get_shops_by_format(vinyl_format):
    """
    Get shops from database by vinyl format.

    Args:
        vinyl_format (str): vinyl format
    Returns:
        list: list of shops
    """

    print("vinyl_format", vinyl_format)
    shops = Shop.get_shops_by_format(vinyl_format)
    print("shops", shops)

    if not shops:
        return {"error": "No shops found for this format"}, 404

    return shops
