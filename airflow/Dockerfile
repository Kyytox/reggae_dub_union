FROM continuumio/miniconda3:latest

# Set the env variables
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV PATH=/opt/conda/bin:$PATH

# create the airflow user
RUN useradd -m airflow

# Install dependencies
COPY environment.yaml .
RUN conda env create -f environment.yaml \
    && conda clean -afy

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

# Copy Credentials GCP
COPY gcp/gcp_sa_key.json /opt/airflow/gcp/gcp_sa_key.json
RUN chmod 755 /opt/airflow/gcp/gcp_sa_key.json

# Give airflow ownership of AIRFLOW_HOME
RUN mkdir -p ${AIRFLOW_HOME}
RUN chown -R airflow:airflow ${AIRFLOW_HOME}

# Activate the environment and ensure it's used in subsequent commands
SHELL ["conda", "run", "-n", "env_reg_dub_airflow", "/bin/bash", "-c"]

# Set the working directory
USER airflow
WORKDIR ${AIRFLOW_HOME}

# Expose the port the app runs on
EXPOSE 8080

# Execute the entrypoint script
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
