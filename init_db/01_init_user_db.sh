#!/bin/bash
set -e

# ----------------------------------------------------------------------
# A. CREATE USER AND THE NEW PROJECT DATABASE
# Connects to the default maintenance DB ($POSTGRES_DB) to perform global operations.
# ----------------------------------------------------------------------
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	    -- 1. Create the application user
			CREATE USER $PROJECT_DB_USER WITH PASSWORD '$PROJECT_DB_PASSWORD';

	    -- 2. Create the new project database and assign ownership
	    CREATE DATABASE $PROJECT_DB_NAME OWNER $PROJECT_DB_USER;
		    
	    -- 3. Grant connection privileges on the database
	    GRANT ALL PRIVILEGES ON DATABASE $PROJECT_DB_NAME TO $PROJECT_DB_USER;

EOSQL

# ----------------------------------------------------------------------
# B. CONFIGURE SCHEMA PRIVILEGES
# Connects DIRECTLY to the newly created project database ($PROJECT_DB_NAME)
# ----------------------------------------------------------------------
echo "Configuring privileges for $PROJECT_DB_NAME..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$PROJECT_DB_NAME" <<-EOSQL

	    -- 1. Grant USAGE and CREATE rights on the 'public' schema
	    -- This is essential so the application user can create tables later.
	    GRANT USAGE, CREATE ON SCHEMA public TO $PROJECT_DB_USER;
	    
	    -- 2. Configure default privileges for future objects created by this user
	    ALTER DEFAULT PRIVILEGES FOR USER $PROJECT_DB_USER IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO $PROJECT_DB_USER;
	    ALTER DEFAULT PRIVILEGES FOR USER $PROJECT_DB_USER IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO $PROJECT_DB_USER;
	    
EOSQL

# ----------------------------------------------------------------------
# C. EXECUTE SCHEMA/DATA SCRIPTS (If files are present)
# Executes subsequent .sql files against the new project database.
# ----------------------------------------------------------------------

# 1. Conditional Data Import: Check for a full database dump first, then fall back to simple inserts.
if [ -f "/docker-entrypoint-initdb.d/sql/02_import_data.sql" ]; then
	echo "Found full import_data.sql. Running full dump on $PROJECT_DB_NAME"
	# Execute the full dump file (e.g., created by pg_dump -F p)
	psql -v ON_ERROR_STOP=1 --username "$PROJECT_DB_USER" --dbname "$PROJECT_DB_NAME" -f /docker-entrypoint-initdb.d/sql/02_import_data.sql

# 2. Run create_tables.sql and insert_shops.sql
elif [ -f "/docker-entrypoint-initdb.d/sql/03_create_tables.sql" ] && [ -f "/docker-entrypoint-initdb.d/sql/04_insert_shops.sql" ]; then
	echo "Running 03_create_tables.sql on $PROJECT_DB_NAME"
	psql -v ON_ERROR_STOP=1 --username "$PROJECT_DB_USER" --dbname "$PROJECT_DB_NAME" -f /docker-entrypoint-initdb.d/sql/03_create_tables.sql

	# Insert initial static data
	echo "Running 04_insert_shops.sql on $PROJECT_DB_NAME"
	# Execute the simple insert script (e.g., for initial static data)
	psql -v ON_ERROR_STOP=1 --username "$PROJECT_DB_USER" --dbname "$PROJECT_DB_NAME" -f /docker-entrypoint-initdb.d/sql/04_insert_shops.sql

else
	echo "No initial data script (import_db.sql or create_tables.sql + insert_shops.sql) found. Skipping data import."
fi

echo "Database provisioning completed for $PROJECT_DB_NAME."
