# ToDo List  =====================================================

sys cleanUp:
tcl㉿NB202405232201)-[~/…/office/Sem-2/FinalYrProject/FleetMIS]
└─$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3  # Only if it's okay to wipe DB
python manage.py makemigrations
python manage.py migrate

# ToDo List Pendings  =============================================

  Some pending functionalities:
  
  ** ** Final Year Project report ** 

# ToDo List Pendings  =============================================


✅ 1. Prerequisites PACKAGES
📌 a) Install Python
On Windows:
Download Python from: https://www.python.org/downloads/

During installation:

✅ Check “Add Python to PATH”

Choose “Customize installation” and ensure pip and venv are selected.

# ToDo List Pendings  =============================================

On Linux (Ubuntu/Debian):
sudo apt update
sudo apt install python3 python3-pip virtualenv -y
python --version       # Or python3 --version on Linux
pip --version          # Or pip3 --version on Linux
python -m pip install --upgrade pip

✅ 2. Create and Activate a Virtual Environment
On Windows:
python -m venv env
env\Scripts\activate

On Linux:
python3 -m venv env
or
virtualenv myenvironment
source env/bin/activate

# Ensure u have git:
apt install git

✅ 3. Install Django and Required Packages

# Core Django
pip install django

# Django REST framework (API development)
pip install djangorestframework

# CORS headers (handling cross-origin resource sharing)
pip install django-cors-headers

# Crispy Forms and Bootstrap styling
pip install django-crispy-forms
pip install crispy-bootstrap4
pip install crispy-bootstrap5

# Admin interface enhancement (optional)
pip install -U django-jazzmin

# PostgreSQL database driver (if using PostgreSQL)
pip install psycopg2-binary

# PDF generation and reporting
pip install reportlab
pip install xhtml2pdf

🧰 Step 4: Update and install VS Code
sudo apt update
sudo apt install code -y

python manage.py runserver
# ToDo List Pendings  =============================================
✅ To Install PostgreSQL and psql (Client) on Ubuntu
Step 1: Update packages
sudo apt update
Step 2: Install PostgreSQL server + client
sudo apt install postgresql postgresql-client -y
# confirm whether PostgreSql is installed:
   which psql
   # You should now see:
   /usr/bin/psql


   # Then check the status
   sudo systemctl status postgresql
   #If you see inactive, dead, or failed, start it with:
   sudo systemctl start postgresql
   # To prevent this issue at boot, enable it:
   sudo systemctl enable postgresql
   # Check if the PostgreSQL server is running
   ps aux | grep postgres
   # Login to PostgreSQL as the default user
sudo -u postgres psql

# Create a new database
CREATE DATABASE fleetmisdb;

# Create a new user
CREATE USER fleetuser WITH PASSWORD '';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE fleetmisdb TO fleetuser;

# Exit PostgreSQL
\q

# then Update settings.p:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fleetmisdb',
        'USER': 'fleetuser',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# Ensure that you make some permision grantings to the the user:
sudo -u postgres psql
-- STEP 1: Connect to the database
\c fleetmisdb
# you should see something like this below:
You are now connected to database "fleetmisdb" as user "postgres".


-- STEP 2: Grant privileges on the schema
GRANT ALL ON SCHEMA public TO fleetuser;

-- STEP 3: Optional but recommended: make fleetuser the owner of the schema
ALTER SCHEMA public OWNER TO fleetuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fleetuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fleetuser;


✅ Then:
Apply migrations:

========================= ADDITIONAL REQUIREMENTS ================== 
3. ✅ Ensure UFW (Ubuntu Firewall) Allows Port 8000
If UFW is enabled (check with sudo ufw status), then allow Django’s port:
sudo ufw allow 8000/tcp

Also, make sure SSH and PostgreSQL are not blocked:
sudo ufw allow OpenSSH
sudo ufw allow 5432/tcp  # if needed for remote DB access
=====================================================================

  # Then Download and Install: 'DBeaver' and alternative for db.sqlite3, for browsing and visualizing the DATABASE ie (fleetmis)
DBeaver CE (Recommended) – GUI 
🔹 Features:
Cross-platform (Linux, Windows, macOS)

Supports PostgreSQL, MySQL, SQLite, etc.

User-friendly GUI

No complicated setup

# Installation procedures:
sudo apt update
sudo apt install default-jdk wget -y
wget https://dbeaver.io/files/dbeaver-ce_latest_amd64.deb
sudo apt install ./dbeaver-ce_latest_amd64.deb

# Launching it:

dbeaver

==========================================================================================

==========================================================================================
            SERVER SETTINGS
==========================================================================================
nano /etc/apache2/sites-available/fleetmis.conf

<VirtualHost *:80>
    ServerName fleetmis.utcl.co.ug

    # Redirect all HTTP traffic to HTTPS
    Redirect "/" "https://fleetmis.utcl.co.ug/"
</VirtualHost>

<VirtualHost *:443>
    ServerName fleetmis.utcl.co.ug

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/fleetmis_utcl.crt
    SSLCertificateKeyFile /etc/ssl/private/fleetmis_utcl.key
    SSLCertificateChainFile /etc/ssl/certs/DigiCertCA.crt

    # Tell backend that client is using HTTPS (prevents redirect loop)
    RequestHeader set X-Forwarded-Proto "https"

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8556/
    ProxyPassReverse / http://127.0.0.1:8556/

    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

    # Optional: Log files (for debugging)
    ErrorLog ${APACHE_LOG_DIR}/fleetmis_error.log
    CustomLog ${APACHE_LOG_DIR}/fleetmis_access.log combined
</VirtualHost>
=================================================================================================

Activate UFW and allow only necessary ports:



# ToDo List Pendings  =============================================

Alternatively USE the script:
📌 Notes:
This script is for Ubuntu/Debian Linux. For Windows, manual steps or PowerShell alternatives can be provided.

It includes interactive prompts for the PostgreSQL password and Django project name.

You’ll need superuser privileges (sudo) for package installations and PostgreSQL configuration.

# ToDo List Pendings  =============================================
Usage Instructions
Save the script as fleetmis_setup.sh

Make it executable:

chmod +x fleetmis_setup.sh
Run the script:
./fleetmis_setup.sh
# ToDo List Pendings  =============================================
