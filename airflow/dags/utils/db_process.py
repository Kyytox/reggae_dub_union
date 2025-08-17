import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from utils.db_connect import db_connect_postgres


def get_shops_from_db(conn) -> pd.DataFrame:
    """
    Get all shops from the database.

    Args:
        conn: Database connection object.

    Returns:
        pd.DataFrame: DataFrame containing all shops with columns (name_shop, name_function, links).
    """

    query = "SELECT * FROM shops"
    df = pd.read_sql(query, conn)

    return df


def get_shop_infos(conn, name_shop: str) -> pd.DataFrame:
    """
    Get links and infos for a specific shop from the database.

    Args:
        conn: Database connection object.
        name_shop (str): Name of the shop to retrieve links for.

    Returns:
        pd.DataFrame: DataFrame containing the shop's information and associated vinyls.
    """

    # Chcek if data exist in vinyls table
    query = """SELECT COUNT(*) 
            FROM vinyls 
            WHERE shop_link_id IN (
                SELECT shop_link_id 
                FROM shops_links
                WHERE shop_id = (
                    SELECT shop_id 
                    FROM shops
                    WHERE shop_name = %s))"""
    count = pd.read_sql(query, conn, params=(name_shop,)).iloc[0, 0]

    if count == 0:
        query = """
        SELECT
            s.shop_id,
            s.shop_name,
            s.shop_nb_min_pages,
            s.shop_nb_max_pages,
            sl.shop_link,
            sl.shop_link_id,

            NULL AS vinyl_id,
            NULL AS vinyl_reference
        FROM shops s
        LEFT JOIN shops_links sl ON s.shop_id = sl.shop_id
        WHERE s.shop_name = %s
        """
    else:
        query = """
            SELECT
                s.shop_id,
                s.shop_name,
                s.shop_nb_min_pages,
                s.shop_nb_max_pages,
                sl.shop_link,
                sl.shop_link_id,
                v.vinyl_id,
                v.vinyl_reference
            FROM shops s
            LEFT JOIN shops_links sl ON s.shop_id = sl.shop_id
            LEFT JOIN vinyls v ON sl.shop_link_id = v.shop_link_id
            WHERE
                s.shop_name = %s
                AND v.vinyl_id = (
                    SELECT MAX(v2.vinyl_id)
                    FROM vinyls v2
                    WHERE v2.shop_link_id = v.shop_link_id
        )    """

    df = pd.read_sql(query, conn, params=(name_shop,))

    return df
