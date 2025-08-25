from flask import request
from app import app
import pandas as pd

from models.models import Vinyl

from utils.libs import format_return_data


@app.route("/get_all_formats", methods=["GET"])
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


@app.route("/get_nb_vinyls", methods=["GET"])
def get_nb_vinyls():
    """
    Get number of vinyls in database.

    Returns:
        int: number of vinyls
    """

    nb_vinyls = Vinyl.get_nb_vinyls()
    return {"nb_vinyls": nb_vinyls}


@app.route("/get_vinyls_songs", methods=["GET"])
def get_vinyls_songs():
    """
    Get all vinyls and songs from database.

    Returns:
        list: list of vinyls and songs
    """

    shops = request.args.getlist("shops[]")
    formats = request.args.getlist("formats[]")
    num_page = int(request.args.get("num_page", 1))
    print("Requested page number:", num_page)

    nb_elem_page_base = 25
    nb_elem_page_max = num_page * nb_elem_page_base
    nb_elem_page_min = (nb_elem_page_max - nb_elem_page_base) + 1

    base_query = """
        WITH vinyls_ranked AS (
            SELECT
                v.*,
                ROW_NUMBER() OVER (
                    PARTITION BY v.shop_link_id
                    ORDER BY v.vinyl_id DESC
                ) AS idx_elem
            FROM public.vinyls v
            """

    end_query = """
        )
        SELECT
            v.vinyl_id,
            v.shop_id,
            v.shop_link_id,
            v.vinyl_format,
            v.vinyl_title,
            v.vinyl_image,
            v.vinyl_price,
            v.vinyl_currency,
            v.vinyl_reference,
            v.vinyl_link,
            s.song_id,
            s.song_title,
            s.song_mp3,
            sh.shop_name
        FROM vinyls_ranked v
        LEFT JOIN public.songs s ON s.vinyl_id = v.vinyl_id
        LEFT JOIN public.shops sh ON v.shop_id = sh.shop_id
        WHERE v.idx_elem BETWEEN %d AND %d
        ORDER BY v.shop_link_id, v.vinyl_id DESC;
        """ % (
        nb_elem_page_min,
        nb_elem_page_max,
    )

    if shops:
        print("Filtering by shops:", shops)
        shops_str = ",".join(f"'{shop}'" for shop in shops)
        base_query += f" WHERE v.shop_id IN ({shops_str})"

    if formats:
        print("Filtering by formats:", formats)
        formats_str = ",".join(f"'{fmt}'" for fmt in formats)
        if shops:
            base_query += f" AND v.vinyl_format IN ({formats_str})"
        else:
            base_query += f" WHERE v.vinyl_format IN ({formats_str})"

    full_query = base_query + end_query

    df = pd.read_sql(full_query, con=app.config["SQLALCHEMY_DATABASE_URI"])

    if df.empty:
        return {"error": "No data found"}

    data = format_return_data(df)

    return data
