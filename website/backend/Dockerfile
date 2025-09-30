FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /app

# Copy the environment file
COPY environment.yaml .

# Copy the rest of the application code
COPY . .

# Install dependencies
RUN conda env create -f environment.yaml

# Activate the environment and ensure it's used in subsequent commands
SHELL ["conda", "run", "-n", "env_reg_dub_back", "/bin/bash", "-c"]

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
CMD ["conda", "run", "--no-capture-output", "-n", "env_reg_dub_back", "gunicorn", "--workers", "4", "--bind", "0.0.0.0:5001", "app:app"]
# CMD ["conda", "run", "--no-capture-output", "-n", "env_reg_dub_back", "flask", "run", "--debug", "--host=0.0.0.0", "--port=5001"]
