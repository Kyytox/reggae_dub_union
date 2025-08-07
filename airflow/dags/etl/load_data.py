import io
import pandas as pd


from utils.utils_gcp_storage import (
    download_blob_into_memory,
    list_blobs_with_prefix,
)

from utils.db_connect import (
    db_connect_postgres,
    get_shop_infos,
    get_shops_links,
    get_shops_from_db,
)

from utils.libs import save_file
from utils.variables import lst_formats_accepted

from airflow.models import Variable


def load_data_to_db(bucket_name: str, time_file_name: str, conn_id: str) -> None:
    """
    Load data from GCP Storage to the database.

    Args:
        bucket_name (str): Name of the GCP Storage bucket.
        time_file_name (str): Timestamp for file naming.
        conn_id (str): Airflow connection ID for the PostgreSQL database.
    """

    # Download the blob into memory
    path_file = f"extract_{time_file_name}/trf_all_shops.csv"
    data = download_blob_into_memory(bucket_name, path_file)
    df = pd.read_csv(io.BytesIO(data))

    # FIX remove this when name will be fixed
    df.rename(columns={"name_shop": "shop_name"}, inplace=True)
    df.rename(columns={"vinyl_ref": "vinyl_reference"}, inplace=True)
    df.rename(columns={"mp3_title": "song_title"}, inplace=True)
    df.rename(columns={"mp3_link": "song_mp3"}, inplace=True)
    # FIX 

    print("Data loaded from GCP Storage:")
    print(df.head())

    df_shops = get_shops_from_db(conn_id)
    print("all shop")
    print(df_shops)

    # join data with shops
    df = df.merge(df_shops, on="shop_name", how="left").drop("shop_function", axis=1)
    print("Data after merging with shops:")
    print(df.head())

    # Identify vinyls data
    df_vinyls = df[
        [
            "shop_id",
            "vinyl_format",
            "vinyl_title",
            "vinyl_image",
            "vinyl_price",
            "vinyl_currency",
            "vinyl_reference",
            "vinyl_url",
        ]
    ]

    return
