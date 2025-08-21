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

    query = """
    select 
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
    from public.songs s
    left join public.vinyls v on s.vinyl_id = v.vinyl_id
    left join public.shops sh on v.shop_id = sh.shop_id
    --where v.shop_id = 3
    order by s.song_id desc
    limit 1000
    """

    df = pd.read_sql(query, con=app.config["SQLALCHEMY_DATABASE_URI"])

    if df.empty:
        return {"error": "No data found"}

    data = format_return_data(df)

    return data
