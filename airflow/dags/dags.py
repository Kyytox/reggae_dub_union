from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
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
    "start_date": datetime(2021, 10, 1),
    "email_on_retry": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="vinyls",
    default_args=default_args,
    description="DAG for scrap vinyls",
    schedule_interval=None,
    tags=["vinyls"],
) as dag:
    create_tables = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="postgres_default",
        sql="sql_init.sql",
    )

    start = BashOperator(
        task_id="start",
        bash_command="echo Start",
    )

    create_tables >> start
