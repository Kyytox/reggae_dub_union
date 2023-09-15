from datetime import datetime, timedelta
from textwrap import dedent


from airflow import DAG

# Operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from operators.extract_data import extract_data
from operators.transform_data import transform_tables

# export AIRFLOW_CONN_POSTGRES_DEFAULT='postgresql://postgres:admin@localhost:5432/vinyls_dub_scrap'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 10, 1),
    "email_on_retry": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="xxxxx",
    default_args=default_args,
    description="DAG for xxxxxx",
    schedule_interval=None,
    tags=["xxxxx"],
) as dag:
    dag.doc_md = """
    # DAG for scrap vinyls from shops

    ## Tasks

    ### create_tables

    - Create tables in database
    - Insert data in shops table

    ### extract__vinyls_from_web

    - Collect shops to scrap
    - Browse shops
    - Scrap shop
    - Insert data in extract_vinyls_temp table

    ### transform_tables

    - Transform data from extract_vinyls_temp to vinyls, songs    
    """

    create_tables = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="postgres_default",
        sql="sql_init.sql",
    )

    extract_from_web = PythonOperator(
        task_id="extract__vinyls_from_web",
        python_callable=extract_data,
    )

    transform_tables = PythonOperator(
        task_id="transform_tables",
        python_callable=transform_tables,
    )

    create_tables >> extract_from_web >> transform_tables
