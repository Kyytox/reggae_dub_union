import io
import pandas as pd

from airflow.models import Variable

from utils.utils_gcp_storage import (
    download_blob_into_memory,
    list_blobs_with_prefix,
    delete_blob,
)

from utils.db_connect import db_connect_postgres


from utils.db_process import (
    get_shops_from_db,
)

from utils.libs import format_path_file


def load_data_to_db(bucket_name: str, time_file_name: str, conn_id: str) -> None:
    """
    Load data from GCP Storage to the database.

    Args:
        bucket_name (str): Name of the GCP Storage bucket.
        time_file_name (str): Timestamp for file naming.
        conn_id (str): Airflow connection ID for the PostgreSQL database.
    """

    # Download the blob into memory
    file_name = "trf_all_shops"
    path_file = format_path_file(time_file_name, file_name)

    # List all blobs with the prefix
    data = download_blob_into_memory(bucket_name, path_file)
    df = pd.read_csv(io.BytesIO(data))

    print("Data loaded from GCP Storage:")
    print(df.head())

    # connection to db
    conn = db_connect_postgres(conn_id)

    # get shops
    df_shops = get_shops_from_db(conn)
    print("all shop")
    print(df_shops)

    # join data with shops
    df = df.merge(df_shops, on="shop_name", how="left").drop("shop_function", axis=1)
    print("Data after merging with shops:")
    print(df.head())

    # prepare df_vinyls
    df_vinyls = (
        df[
            [
                "shop_id",
                "shop_link_id",
                "vinyl_format",
                "vinyl_title",
                "vinyl_image",
                "vinyl_price",
                "vinyl_currency",
                "vinyl_reference",
                "vinyl_link",
            ]
        ]
        .copy()
        .drop_duplicates()
    )

    # Insert in vinyls table and return vinyl_id
    try:
        lst_vinyl_ids = []

        cursor = conn.cursor()

        # Insert vinyls into the Vinyls table
        for _, row in df_vinyls.iterrows():
            query = """
                INSERT INTO vinyls (shop_id, shop_link_id, vinyl_format, vinyl_title, vinyl_image, vinyl_price, vinyl_currency, vinyl_reference, vinyl_link)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING vinyl_id;
            """
            params = (
                row["shop_id"],
                row["shop_link_id"],
                row["vinyl_format"],
                row["vinyl_title"],
                row["vinyl_image"],
                row["vinyl_price"],
                row["vinyl_currency"],
                row["vinyl_reference"],
                row["vinyl_link"],
            )
            cursor.execute(query, params)
            vinyl_id = cursor.fetchone()[0]
            lst_vinyl_ids.append(vinyl_id)

        # Rattach vinyl_id to the original DataFrame
        df_vinyls["vinyl_id"] = lst_vinyl_ids

        # Rattach vinyl_id to df_songs
        df = df.merge(
            df_vinyls[
                [
                    "vinyl_id",
                    "shop_id",
                    "shop_link_id",
                    "vinyl_reference",
                    "vinyl_link",
                ]
            ],
            on=[
                "shop_id",
                "shop_link_id",
                "vinyl_reference",
                "vinyl_link",
            ],
            how="left",
        )

        # Insert songs into the Songs table
        for _, row in df.iterrows():
            query = """
                INSERT INTO songs (vinyl_id, song_title, song_mp3)
                VALUES (%s, %s, %s);
            """
            params = (row["vinyl_id"], row["song_title"], row["song_mp3"])
            cursor.execute(query, params)

        # Commit the transaction
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        print("Data loaded into the database successfully.")
        print("Number of records inserted:", len(df))

    # Delete the file from GCP Storage
    delete_blob(bucket_name, path_file)

    return
