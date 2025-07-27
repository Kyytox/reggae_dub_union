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


def get_shops_from_db(conn) -> pd.DataFrame:
    """
    Get all shops from the database.

    Args:
        conn: Connection object to the PostgreSQL database.

    Returns:
        pd.DataFrame: DataFrame containing all shops with columns (name_shop, name_function, links).
    """

    query = "SELECT * FROM shops"
    df = pd.read_sql(query, conn)

    return df


def get_specific_shop_links(conn, shop_name: str) -> pd.DataFrame:
    """
    Get links for a specific shop from the database.

    Args:
                conn: Connection object to the PostgreSQL database.
                shop_name (str): Name of the shop to retrieve links for.

    Returns:
            pd.DataFrame: DataFrame containing links for the specified shop.
    """
    query = "SELECT * FROM shops WHERE name_shop = %s"
    df = pd.read_sql(query, conn, params=(shop_name,))

    return df
