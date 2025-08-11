import pandas as pd
from datetime import datetime, timedelta

from airflow.sdk import DAG, task, task_group, get_current_context
from airflow.utils.task_group import TaskGroup

# Operators
# from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from airflow.models import Variable


from utils.variables import (
    BUCKET_NAME,
    CONNECTION_DB,
)

from etl.extract_data import (
    scrap_jahwaggysrecords,
    scrap_onlyrootsreggae,
    scrap_controltower,
    scrap_reggaefever,
    scrap_pataterecords,
    scrap_lionvibes,
    scrap_toolboxrecords,
    scrap_reggaemuseum,
)

from utils.db_connect import db_connect_postgres
from utils.db_process import get_shops_from_db

from etl.transform_data import transform_data
from etl.load_data import load_data_to_db


default_args = {
    "owner": "admin",
    # "depends_on_past": False,
    # "start_date": datetime(2026, 1, 1),
    # "email_on_retry": False,
    # "email_on_failure": False,
    # "email_on_retry": False,
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="init_database",
    default_args=default_args,
    description="DAG for initializing the database",
    tags=["database", "initialization"],
    catchup=False,
) as dag:
    dag.doc_md = """
    # DAG for initializing the database

    ## Tasks

    - Create the connection to the database
    - Create tables in the database
    - Insert data in the shops table
    """

    init_db = SQLExecuteQueryOperator(
        task_id="init_db",
        conn_id="con_reggae_dub_union_db",
        sql="sql/sql_init.sql",
    )
    insert_shops = SQLExecuteQueryOperator(
        task_id="insert_shops",
        conn_id="con_reggae_dub_union_db",
        sql="sql/insert_shops.sql",
    )

    init_db >> insert_shops


with DAG(
    dag_id="dump_database",
    default_args=default_args,
    description="DAG for dumping the database",
    tags=["database", "dump"],
    catchup=False,
) as dag:
    dag.doc_md = """
    # DAG for dumping the database

    ## Tasks

    - Delete Tables in the database
    """

    delete_db = SQLExecuteQueryOperator(
        task_id="dump_db",
        conn_id="con_reggae_dub_union_db",
        sql="sql/dump_db.sql",
    )

    delete_db


with DAG(
    dag_id="etl_vinyls_from_shops",
    default_args=default_args,
    description="DAG for Extracting, Transforming and Loading vinyls from shops",
    schedule=None,
    tags=["etl"],
    catchup=False,
) as dag:
    dag.doc_md = """
    # DAG for Extracting, Transforming and Loading vinyls from shops

        # df = df.json()
        # return df
    ## Tasks

    ### Extract
    - Collect shops to scrap
    - Browse shops
    - Scrap shop
    - Save data in cloud Storage in parquet format
    
    ### Transform
    - Get data from cloud Storage
    - Transform data

    ### Load
    - Load transformed data in Cloud SQL

    """

    def get_shop_list(conn_id: str):
        """
        Get the list of shops from the database.

        Args:
        conn_id (str): Airflow connection ID for the PostgreSQL database.

        Returns:
        df (pd.DataFrame): DataFrame containing the shop list with columns (shop_name, scrap_function).

        """
        conn = db_connect_postgres(conn_id)
        cur = conn.cursor()

        # Check if Table shops exists
        query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'shops');"
        result = pd.read_sql(query, conn).iloc[0, 0]

        if not result:
            # raise ValueError("Table 'shops' does not exist in the database.")
            return pd.DataFrame()

        df = get_shops_from_db(conn)
        print(df)
        cur.close()
        conn.close()
        return df

    # Define var timestamp for file naming
    time_file_name = datetime.now().strftime("%Y%m%d_%H")
    Variable.set(key="time_file_name", value=time_file_name)

    conn_id = Variable.get("conn_id", default_var=CONNECTION_DB)
    bucket_name = Variable.get("bucket_name", default_var=BUCKET_NAME)

    # Create a task for each shop using PythonOperator
    with TaskGroup("tsk_gp") as tsk_gp:
        # Get the list of shops from the database
        shop_list = get_shop_list(conn_id)

        for index, row in shop_list.iterrows():
            name_shop = row["shop_name"]
            scrap_function = row["shop_function"]

            PythonOperator(
                task_id=f"tsk_scrap_{name_shop}",
                python_callable=eval(scrap_function),
                op_kwargs={
                    "name_shop": name_shop,
                    "conn_id": conn_id,
                    "bucket_name": bucket_name,
                    "time_file_name": time_file_name,
                },
            )

    # Task Transform Data
    tsk_transform_data = PythonOperator(
        task_id="tsk_transform_data",
        python_callable=transform_data,
        op_kwargs={
            "bucket_name": bucket_name,
            "time_file_name": time_file_name,
        },
    )

    # Task Load Data to DB
    tsk_load_data = PythonOperator(
        task_id="tsk_load_data",
        python_callable=load_data_to_db,
        op_kwargs={
            "bucket_name": bucket_name,
            "time_file_name": time_file_name,
            "conn_id": conn_id,
        },
    )

    # Run all scrap tasks
    (tsk_gp >> tsk_transform_data >> tsk_load_data)
