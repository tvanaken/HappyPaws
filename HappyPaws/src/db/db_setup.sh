# This script creates a new database user (from .env file)
# that has "create database" privileges. Application databases 
# (production + test) will be built via SQLAlchemy scripts:
echo "$PWD"
echo "$(ls -la)"
pg_pass=$(cat ./.env | grep PGPASSWORD | awk -F= '{print $2}')
DB_USERNAME=$(cat ./.env | grep DB_USERNAME | awk -F= '{print $2}')
DB_PASSWORD=$(cat ./.env | grep DB_PASSWORD | awk -F= '{print $2}')
DB_HOST=$(cat ./.env | grep DB_HOST | awk -F= '{print $2}')
DB_PORT=$(cat ./.env | grep DB_PORT | awk -F= '{print $2}')

# Set the postgres password environment variable
export PGPASSWORD=$pg_pass

# Create new DB user with appropriate permissions:
psql -U postgres -h $DB_HOST -p $DB_PORT -c "CREATE USER "$DB_USERNAME" with encrypted password '"$DB_PASSWORD"';"
psql -U postgres -h $DB_HOST -p $DB_PORT -c "GRANT USAGE ON SCHEMA public TO "$DB_USERNAME";"
psql -U postgres -h $DB_HOST -p $DB_PORT -c "ALTER USER "$DB_USERNAME" CREATEDB;"
