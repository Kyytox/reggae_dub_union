#!/bin/bash

# wait for Postgres to be ready
# while ! nc -z postgres 5433; do
# 	sleep 1
# done

# Activate conda environment
source /opt/conda/bin/activate env_reg_dub_airflow

# Init database Airflow
airflow db init
airflow db upgrade

# Create admin user if not exists
airflow users create \
	--username admin \
	--firstname Admin \
	--lastname User \
	--role Admin \
	--email admin@example.com \
	--password admin ||
	true # Ignore error if user already exists

# Start Service according to the command line in the docker-compose file
exec airflow "$@"
