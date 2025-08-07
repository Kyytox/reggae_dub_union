import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def db_connect_postgres(con_id: str):
    """
    Connect to the PostgreSQL database using Airflow's PostgresHook.

    Args:
        con_id (str): Airflow connection ID for the PostgreSQL database.

    Returns:
        Connection object to the PostgreSQL database.
    """
    try:
        postgres_hook = PostgresHook(postgres_conn_id=con_id)
        conn = postgres_hook.get_conn()
    except Exception as e:
        raise Exception(f"Failed to connect to the database: {e}")

    return conn


def get_shops_from_db(conn_id) -> pd.DataFrame:
    """
    Get all shops from the database.

    Args:
        conn_id: id of the Airflow connection to the PostgreSQL database.

    Returns:
        pd.DataFrame: DataFrame containing all shops with columns (name_shop, name_function, links).
    """

    conn = db_connect_postgres(conn_id)

    query = "SELECT * FROM shops"
    df = pd.read_sql(query, conn)

    conn.close()

    return df


def get_shops_links(df_shops: pd.DataFrame) -> list:
    """
    Get links for all shops from the DataFrame.

    Args:
        df_shops (pd.DataFrame): DataFrame containing shop information.

    Returns:
        list: List of URLs for all shops.
    """
    if "shop_link" not in df_shops.columns:
        raise ValueError("DataFrame does not contain 'shop_link' column")

    lst_urls = df_shops["shop_link"].dropna().tolist()

    if not lst_urls:
        raise ValueError("No links found in the DataFrame")

    return lst_urls


def get_shop_infos(conn_id: str, name_shop: str) -> pd.DataFrame:
    """
    Get links and infos for a specific shop from the database.

    Args:
        conn_id (str): Airflow connection ID for the PostgreSQL database.
        name_shop (str): Name of the shop to retrieve links for.

    Returns:
        pd.DataFrame: DataFrame containing the shop's information and associated vinyls.
    """

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    query = """
        SELECT s.*, v.*
        FROM shops s
        LEFT JOIN shops_links sl ON s.shop_id = sl.shop_id
        LEFT JOIN vinyls v ON s.shop_id = v.shop_id
        WHERE s.shop_name = %s
    """

    df = pd.read_sql(query, conn, params=(name_shop,))

    conn.close()

    return df
