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
