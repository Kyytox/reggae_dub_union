from app import app
import pandas as pd

from utils.libs import format_return_data


@app.route("/get_vinyls_songs", methods=["GET"])
def get_vinyls_songs():
    """
    Get all vinyls and songs from database.

    Returns:
        list: list of vinyls and songs
    """

    # query = """
    # select
    #     v.vinyl_id,
    #     v.shop_id,
    #     v.shop_link_id,
    #     v.vinyl_format,
    #     v.vinyl_title,
    #     v.vinyl_image,
    #     v.vinyl_price,
    #     v.vinyl_currency,
    #     v.vinyl_reference,
    #     v.vinyl_link,
    #     s.song_id,
    #     s.song_title,
    #     s.song_mp3,
    #     sh.shop_name
    # from public.songs s
    # left join public.vinyls v on s.vinyl_id = v.vinyl_id
    # left join public.shops sh on v.shop_id = sh.shop_id
    # order by s.song_id desc
    # limit 1000
    # """
    # --where v.shop_id = 3
    query = """
        WITH vinyls_ranked AS (
            SELECT
                v.*,
                ROW_NUMBER() OVER (
                    PARTITION BY v.shop_link_id
                    ORDER BY v.vinyl_id DESC
                ) AS rn
            FROM public.vinyls v
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
        WHERE v.rn <= 25
        ORDER BY v.shop_link_id, v.vinyl_id DESC;
    """
    # ROW_NUMBER() OVER (ORDER BY v.shop_link_id, v.vinyl_id DESC) AS id_elem

    df = pd.read_sql(query, con=app.config["SQLALCHEMY_DATABASE_URI"])

    if df.empty:
        return {"error": "No data found"}

    data = format_return_data(df)

    return data
