import pandas as pd
from app import app
from app import db
from models.models import Vinyl, Song, Shop
from utils.libs import format_return_data


@app.route("/search/<search>", methods=["GET"])
def search(search):
    """
    Search for vinyls and songs in the database.

    Args:
        search (str): search

    Returns:
        list: list of vinyls and songs matching the search term
        dict: error message if search term is invalid or an error occurs
    """
    # search = search.strip()
    if not search or len(search) > 100:
        return {"error": "Search term is too short or too long"}

    try:
        # get vinyls and songs from database with search in title, song title
        req = (
            db.session.query(
                Vinyl.vinyl_id,
                Vinyl.shop_id,
                Vinyl.shop_link_id,
                Vinyl.vinyl_format,
                Vinyl.vinyl_title,
                Vinyl.vinyl_image,
                Vinyl.vinyl_price,
                Vinyl.vinyl_currency,
                Vinyl.vinyl_reference,
                Vinyl.vinyl_link,
                Song.song_id,
                Song.song_title,
                Song.song_mp3,
                Shop.shop_name,
            )
            .outerjoin(Song, Song.vinyl_id == Vinyl.vinyl_id)
            .outerjoin(Shop, Vinyl.shop_id == Shop.shop_id)
            .filter(
                Vinyl.vinyl_title.ilike(f"%{search}%")
                | Song.song_title.ilike(f"%{search}%")
            )
            .order_by(Song.song_id.desc())
        ).limit(1000)

        # convert to def
        result = []
        for (
            vinyl_id,
            shop_id,
            shop_link_id,
            vinyl_format,
            vinyl_title,
            vinyl_image,
            vinyl_price,
            vinyl_currency,
            vinyl_reference,
            vinyl_link,
            song_id,
            song_title,
            song_mp3,
            shop_name,
        ) in req:
            result.append(
                {
                    "vinyl_id": vinyl_id,
                    "shop_id": shop_id,
                    "shop_link_id": shop_link_id,
                    "vinyl_format": vinyl_format,
                    "vinyl_title": vinyl_title,
                    "vinyl_image": vinyl_image,
                    "vinyl_price": vinyl_price,
                    "vinyl_currency": vinyl_currency,
                    "vinyl_reference": vinyl_reference,
                    "vinyl_link": vinyl_link,
                    "song_id": song_id,
                    "song_title": song_title,
                    "song_mp3": song_mp3,
                    "shop_name": shop_name,
                }
            )

        df = pd.DataFrame(result)
        if df.empty:
            return {"error": "No results found"}

        data = format_return_data(df)
        return data
    except Exception as e:
        print(f"Error during search: {e}")
        return {"error": "An error occurred during the search. Please try again later."}
