#!/bin/bash
set -e

# Update the system
sudo yum update -y

# Install necessary packages
sudo yum install -y postgresql-server postgresql postgresql-contrib python3-devel postgresql-devel python3 python3-pip unzip gcc

# Unzip the archive to /tmp
sudo unzip /tmp/app.zip -d /tmp

# Move the contents from /tmp to /opt/myapp
sudo mv /tmp/code_files /opt/myapp/
sudo mv /tmp/requirements.txt /opt/myapp/

# Navigate to the target directory and install dependencies
cd /opt/myapp
sudo python3 -m venv venv
source venv/bin/activate
sudo pip3 install -r requirements.txt

# Initialize PostgreSQL database
sudo postgresql-setup --initdb

# Start PostgreSQL service
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Use environment variables for database credentials
if [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_NAME" ]; then
  echo "Database credentials are not set. Please configure DB_USER, DB_PASSWORD, and DB_NAME."
  exit 1
fi

sudo su - postgres <<EOF
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
EOF

sudo sed -i 's/\(scram-sha-256\|ident\|peer\)/md5/g' /var/lib/pgsql/data/pg_hba.conf
sudo systemctl restart postgresql


