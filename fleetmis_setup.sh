#!/bin/bash

# Title: FleetMIS Setup Script (Linux - Ubuntu/Debian)
# Author: Abdul-Rasheed Kyazze
# Purpose: Automate the installation of Django, PostgreSQL, required packages, and DBeaver for FleetMIS

echo "========== FLEETMIS SETUP START =========="

# Update system packages
echo "🔄 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python, pip, venv
echo "🐍 Installing Python, pip, and venv..."
sudo apt install python3 python3-pip python3-venv -y

# Verify Python and pip versions
echo "✅ Verifying Python and pip..."
python3 --version
pip3 --version

# Upgrade pip
echo "⬆️ Upgrading pip..."
python3 -m pip install --upgrade pip

# Create and activate virtual environment
echo "📦 Creating virtual environment 'env'..."
python3 -m venv env
source env/bin/activate
echo "✅ Virtual environment activated."

# Install Django and dependencies
echo "📦 Installing Django and related packages..."
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install django-crispy-forms
pip install crispy-bootstrap4
pip install crispy-bootstrap5
pip install -U django-jazzmin
pip install psycopg2-binary
pip install reportlab
pip install xhtml2pdf
pip install virtualenv

# Save requirements
pip freeze > requirements.txt

# Install and configure PostgreSQL
echo "🐘 Installing PostgreSQL..."
sudo apt install postgresql postgresql-contrib -y

# Check PostgreSQL status
echo "🔍 Checking PostgreSQL service..."
which psql
sudo systemctl status postgresql

# Start and enable PostgreSQL
echo "🚀 Starting and enabling PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Prompt for user password
echo "🔐 Enter a password for the PostgreSQL user 'fleetuser':"
read -s POSTGRES_PASSWORD

# Configure PostgreSQL database and user
echo "📁 Setting up PostgreSQL database and user..."
sudo -u postgres psql <<EOF
CREATE DATABASE fleetmisdb;
CREATE USER fleetuser WITH PASSWORD '$POSTGRES_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE fleetmisdb TO fleetuser;
\q
EOF

# Grant schema permissions
echo "🔑 Granting schema privileges..."
sudo -u postgres psql <<EOF
\c fleetmisdb
GRANT ALL ON SCHEMA public TO fleetuser;
ALTER SCHEMA public OWNER TO fleetuser;
\q
EOF

# Display database settings for Django
echo "🔧 Add the following to your Django settings.py DATABASES section:"
echo ""
echo "DATABASES = {"
echo "    'default': {"
echo "        'ENGINE': 'django.db.backends.postgresql',"
echo "        'NAME': 'fleetmisdb',"
echo "        'USER': 'fleetuser',"
echo "        'PASSWORD': '$POSTGRES_PASSWORD',"
echo "        'HOST': 'localhost',"
echo "        'PORT': '5432',"
echo "    }"
echo "}"

# Create Django project (optional)
read -p "🛠️ Do you want to create a Django project now? (y/n): " create_project
if [[ "$create_project" == "y" ]]; then
    read -p "📁 Enter your project name: " project_name
    django-admin startproject $project_name
    cd $project_name
    echo "📂 Django project '$project_name' created."
    echo "🔧 Apply migrations..."
    python manage.py migrate
    echo "🚀 Running development server..."
    python manage.py runserver
fi

# Optional: Install DBeaver
read -p "🖥️ Do you want to install DBeaver for PostgreSQL GUI management? (y/n): " install_dbeaver
if [[ "$install_dbeaver" == "y" ]]; then
    echo "📦 Installing Java JDK (required)..."
    sudo apt install default-jdk wget -y
    echo "📥 Downloading DBeaver..."
    wget https://dbeaver.io/files/dbeaver-ce_latest_amd64.deb
    echo "📦 Installing DBeaver..."
    sudo apt install ./dbeaver-ce_latest_amd64.deb
    echo "✅ DBeaver installed. Launch it by running: dbeaver"
fi

echo "🎉 FleetMIS setup complete!"
echo "========== FLEETMIS SETUP END =========="
