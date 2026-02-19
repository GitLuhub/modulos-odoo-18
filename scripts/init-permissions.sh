#!/bin/bash

set -e

echo "Initializing database permissions..."

psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" <<-EOSQL
    ALTER DATABASE $DB_NAME SET timezone TO 'UTC';
    
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;
    
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "postgis";
EOSQL

echo "Permissions initialized successfully!"
