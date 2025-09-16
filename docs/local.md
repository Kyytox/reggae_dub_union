# Install Local

## PostgreSQL

### Install PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Start PostgreSQL service

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Connect to PostgreSQL

```bash
sudo -i -u postgres
psql
```

### Update user root password

```bash
ALTER USER postgres WITH PASSWORD 'PASSWORD';
```

### Create new user

```bash
CREATE USER kytox WITH PASSWORD 'PASSWORD';
```

### Create the database

```bash
CREATE DATABASE reg_dub_union_db OWNER kytox;
```

### Exit PostgreSQL

```bash
\q
exit
```

### Import your DB in PostgreSQL

```bash
psql -U kytox -d reg_dub_union_db -f import_db.sql
```

### Access your DB

```bash
psql -U kytox -d reg_dub_union_db
```

## Airflow

### Airflow environment

```bash
export AIRFLOW_HOME=path_to_your_airflow_directory
```

### Create Install Conda environment

```bash
conda install -f environment_airflow.yml
conda activate env_reg_dub_airflow
```

### Migrate Airflow DB

Connection to PostgreSQL

```bash
sudo -i -u postgres
psql
```

Create Database, user and password

```sql
CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'PASSWORD';
ALTER DATABASE airflow_db OWNER TO airflow_user;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
GRANT ALL ON SCHEMA public TO airflow_user;
```

Update airflow.cfg

```bash
sql_alchemy_conn = postgresql+psycopg2://airflow_user:PASSWORD@localhost/airflow_db
```

### Create Airflow User

```bash
airflow users create \
    --username kytox \
    --firstname FIRSTNAME \
    --lastname LASTNAME \
    --role Admin \
    --email YOUR_EMAIL
```

### Create Services

```bash
sudo nano /etc/systemd/system/airflow-webserver.service
```

```ini
[Unit]
Description=Airflow webserver daemon
After=network.target

[Service]
Environment="AIRFLOW_HOME=path_to_your_airflow_directory"
User=your_username
Group=your_groupname
Type=simple
ExecStart=path_to_your_conda/bin/airflow webserver
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

```bash
sudo nano /etc/systemd/system/airflow-scheduler.service
```

```ini
[Unit]
Description=Airflow scheduler daemon
After=network.target  

[Service]
Environment="AIRFLOW_HOME=path_to_your_airflow_directory"
User=your_username
Group=your_groupname
Type=simple
ExecStart=path_to_your_conda/bin/airflow scheduler
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### Start Services

```bash
sudo systemctl daemon-reload
sudo systemctl start airflow-webserver
sudo systemctl start airflow-scheduler
sudo systemctl enable airflow-webserver
sudo systemctl enable airflow-scheduler
```

## Backend - Frontend

### Create Conda environment

```bash
conda create -f website/backend/environment.yaml
conda activate env_reg_dub_backend
```

### Environment variables

In .env file

```txt
# JWT
JWT_SECRET_KEY="your_jwt_secret_key"

# Env
FLASK_ENV=production

# DB Connection
SQLALCHEMY_DATABASE_URI="postgresql://user:pwd@localhost/reg_dub_union_db"
```

### Create services

```bash
sudo nano /etc/systemd/system/reg_dub_backend.service
```

```ini
Unit]
Description=Reg_Dub_Backend service
After=network.target

[Service]
User=your_username
Group=your_groupname
WorkingDirectory=/path/reggae_dub_union/website/backend
Environment="PATH=/path/miniconda3/envs/env_reg_dub_back/bin"
ExecStart=/path/miniconda3/envs/env_reg_dub_back/bin/gunicorn -w 3 --bind 0.0.0.0:5001 app:app
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target

```

```bash
sudo systemctl daemon-reload
sudo systemctl start reg_dub_backend
sudo systemctl enable reg_dub_backend
```

### Frontend

Install Node.js and npm

```bash
cd website/frontend
npm install
npm run build
```

Deploy with Pm2

```bash
pm2 serve . 3000 --spa --name "reggaedubunion-frontend"
pm2 save
pm2 startup
```

Reload pm2

```bash
pm2 reload reggaedubunion-frontend
```

### Nginx

```bash
sudo apt install nginx
``` 

```bash
sudo nano /etc/nginx/sites-available/reg_dub_union
```

```nginx
server {

    listen 80;
    server_name reggaedubunion.fr www.reggaedubunion.fr;

    root /path/reggae_dub_union/website/frontend/dist;
    index index.html;

    # Frontend (React)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend Flask
    location /api/ {
        proxy_pass http://0.0.0.0:5001;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/reg_dub_union /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### SSL with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d reggaedubunion.fr -d www.reggaedubunion.fr
```

Check /etc/nginx/sites-available/reg_dub_union if SSL is correctly configured
