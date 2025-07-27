from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.utils.task_group import TaskGroup

# Operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


from airflow.models import Variable


from operators.scripts_scrap import (
    scrap_toolboxrecords,
    scrap_reggaemuseum,
    scrap_reggaefever,
    scrap_pataterecords,
    scrap_onlyrootsreggae,
    scrap_lionvibes,
    scrap_jahwaggysrecords,
    scrap_controltower,
)

from operators.transform_data import transform_data


default_args = {
    "owner": "admin",
    # "depends_on_past": False,
    # "start_date": datetime(2023, 10, 1),
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
    # schedule_interval=None,
    tags=["etl"],
) as dag:
    dag.doc_md = """
    # DAG for Extracting, Transforming and Loading vinyls from shops

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

    # Define var timestamp for file naming
    # time_file_name = datetime.now().strftime("%Y%m%d_%H")
    time_file_name = "20250727_05"
    Variable.set(key="time_file_name", value=time_file_name)

    conn_id = Variable.get("conn_id", default_var="con_reggae_dub_union_db")
    bucket_name = Variable.get("bucket_name", default_var="reggae_dub_union_bucket")

    dict_tasks = {
        # "jahwaggysrecords": scrap_jahwaggysrecords,
        # "onlyrootsreggae": scrap_onlyrootsreggae,
        # "controltower": scrap_controltower,
        # "reggaefever": scrap_reggaefever,
        # "pataterecords": scrap_pataterecords,
        # "toolboxrecords": scrap_toolboxrecords,
        # "lionvibes": scrap_lionvibes,
        # "reggaemuseum": scrap_reggaemuseum,
    }

    # Task Collect Shops to Scrap
    with TaskGroup("scrap_shops") as scrap_shops:
        for name_shop, scrap_function in dict_tasks.items():
            PythonOperator(
                task_id=f"tsk_scrap_{name_shop}",
                python_callable=scrap_function,
                op_kwargs={
                    "name_shop": name_shop,
                    "conn_id": conn_id,
                    "bucket_name": bucket_name,
                },
            )

    # Task Transform Data
    transform_data = PythonOperator(
        task_id="tsk_transform_data",
        python_callable=transform_data,
        op_kwargs={
            "bucket_name": bucket_name,
            "time_file_name": time_file_name,
        },
    )

    # Run all scrap tasks
    # scrap_shops >> transform_data
    transform_data
