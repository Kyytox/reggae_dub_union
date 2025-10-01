#!/bin/bash

# Activate conda environment
source /opt/conda/bin/activate env_reg_dub_airflow

# Init database Airflow
airflow db init
airflow db upgrade

# Create admin user if not exists
airflow users create \
	--username ${AIRFLOW_USERNAME} \
	--firstname Admin \
	--lastname User \
	--role Admin \
	--email admin@example.com \
	--password ${AIRFLOW_PASSWORD} ||
	true # Ignore error if user already exists

# Start Service according to the command line in the docker-compose file
exec airflow "$@"
