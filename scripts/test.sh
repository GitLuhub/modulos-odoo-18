#!/bin/bash

set -e

echo "Running Odoo tests..."

ODOO_VERSION="${ODOO_VERSION:-18}"
DB_NAME="${DB_NAME:-odoo_test}"
DB_USER="${DB_USER:-odoo}"
DB_HOST="${DB_HOST:-localhost}"

echo "Dropping test database if exists..."
dropdb --if-exists -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" || true

echo "Creating test database..."
createdb -h "$DB_HOST" -U "$DB_USER" "$DB_NAME"

echo "Installing module and running tests..."
odoo -d "$DB_NAME" \
    --test-enable \
    --stop-after-init \
    --init custom_module

echo "All tests completed!"
