from flask import request
from app import app
import pandas as pd

from models.models import Vinyl

from utils.libs import format_return_data


def extract_request_data(request):
    """
    Extract data from request.

    Args:
        request (flask.Request): Flask request object

    Returns:
        tuple: (shops, formats, num_page)
    """
    data = {
        "shops": request.args.getlist("shops[]"),
        "formats": request.args.getlist("formats[]"),
        "search": request.args.get("search", ""),
        "num_page": int(request.args.get("num_page", 1)),
        "top_random": request.args.get("top_random"),
    }
    print("Extracted data from request:", data)

    return data


@app.route("/get_nb_vinyls", methods=["GET"])
def get_nb_vinyls():
    """
    Get number of vinyls in database.

    Returns:
        int: number of vinyls
    """

    data = extract_request_data(request)

    nb_vinyls = Vinyl.get_nb_vinyls(
        shops=data["shops"], formats=data["formats"], search=data["search"]
    )
    print("nb_vinyls", nb_vinyls)
    return {"nb_vinyls": nb_vinyls}


def determine_nb_elem_page(shops, formats, num_page):
    """
    Determine number of elements per page.

    Args:
        num_page (int): number of page

    Returns:
        int: number of elements per page
    """
    len_shop = len(shops)
    len_format = len(formats)

    if len_shop == 0 and len_format == 0:
        nb_elem_page_base = 15
    elif len_shop == 1 or len_format == 0:
        nb_elem_page_base = min(100, 50 + ((max(len_shop, len_format)) * 6))
    elif len_shop == 0 or len_format == 1:
        nb_elem_page_base = min(100, 30 + ((max(len_shop, len_format))))
    else:
        nb_elem_page_base = min(100, 70 + ((len_shop) * (len_format) * 4))

    nb_elem_page_max = num_page * nb_elem_page_base
    nb_elem_page_min = (nb_elem_page_max - nb_elem_page_base) + 1

    return nb_elem_page_min, nb_elem_page_max


def query_vinyls_filters(shops, formats, nb_elem_page_min, nb_elem_page_max):
    """
    Create SQL query with filters.

    Args:
        shops (list): list of shops to filter
        formats (list): list of formats to filter
        nb_elem_page_min (int): minimum number of elements per page
        nb_elem_page_max (int): maximum number of elements per page
        top_random (str): order by top or random
    Returns:
        str: SQL query
    """
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
            sh.shop_name,
            sh.shop_real_name
        FROM vinyls_ranked v
        LEFT JOIN public.songs s ON s.vinyl_id = v.vinyl_id
        LEFT JOIN public.shops sh ON v.shop_id = sh.shop_id
        WHERE v.idx_elem BETWEEN %d AND %d
        ORDER BY v.vinyl_id DESC;
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

    return full_query


def query_vinyls_random():
    """
    Create SQL query to get random vinyls.

    Returns:
        str: SQL query
    """
    end_query = """
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
            sh.shop_name,
            sh.shop_real_name 
        FROM vinyls v
        LEFT JOIN public.songs s ON s.vinyl_id = v.vinyl_id
        LEFT JOIN public.shops sh ON v.shop_id = sh.shop_id
        ORDER BY RANDOM()
        LIMIT 100;
        """

    return end_query


@app.route("/get_vinyls_songs", methods=["GET"])
def get_vinyls_songs():
    """
    Get all vinyls and songs from database.

    Returns:
        list: list of vinyls and songs
    """
    # shops, formats, num_page, top_random = extract_request_data(request)
    data = extract_request_data(request)

    nb_elem_page_min, nb_elem_page_max = determine_nb_elem_page(
        data["shops"], data["formats"], data["num_page"]
    )

    if data["top_random"] == "true":
        full_query = query_vinyls_random()
    else:
        full_query = query_vinyls_filters(
            data["shops"], data["formats"], nb_elem_page_min, nb_elem_page_max
        )

    df = pd.read_sql(full_query, con=app.config["SQLALCHEMY_DATABASE_URI"])

    if df.empty:
        print("No data found")
        return {"error": "No data found"}

    data = format_return_data(df)

    return data
