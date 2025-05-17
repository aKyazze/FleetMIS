# ToDo List  =====================================================

sys cleanUp:
tcl㉿NB202405232201)-[~/…/office/Sem-2/FinalYrProject/FleetMIS]
└─$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3  # Only if it's okay to wipe DB
python manage.py makemigrations
python manage.py migrate

PreRequists: PACKAGES

   1 pip install django
   2 pip install -U django-jazzmin
   3 pip install reportlab
   4 pip install django-crispy_forms
   5 pip install crispy-bootstrap5 
   6 pip install django-crispy-forms crispy-bootstrap4
   7 pip install djangorestframework
   8 python manage.py runserver
   9 python installation
   10 pip install psycopg2-binary
   11 pip install django-cors-headers
   12 pip install xhtml2pdf
   13 pip install xhtml2pdf




   # ================== Create a PostgreSQL database and user ========================
   # But Be4, you need to do some checks and confirmation. 

   # confirm whether PostgreSql is installed:
   which psql
   # Then check the status
   sudo systemctl status postgresql
   #If you see inactive, dead, or failed, start it with:
   sudo systemctl start postgresql
   # To prevent this issue at boot, enable it:
   sudo systemctl enable postgresql
   # Check if the PostgreSQL server is running
   ps aux | grep postgres
 # If the out put is like below, you'r perfect and good to go:
 postgres    8616  0.0  0.1 222772 31616 ?        Ss   08:51   0:00 /usr/lib/postgresql/16/bin/postgres -D /var/lib/postgresql/16/main -c config_file=/etc/postgresql/16/main/postgresql.conf
postgres    8617  0.0  0.0 222772  6684 ?        Ss   08:51   0:00 postgres: 16/main: checkpointer 
postgres    8618  0.0  0.0 222908  7964 ?        Ss   08:51   0:00 postgres: 16/main: background writer 
postgres    8620  0.0  0.0 222772 11036 ?        Ss   08:51   0:00 postgres: 16/main: walwriter 
postgres    8621  0.0  0.0 224360  9500 ?        Ss   08:51   0:00 postgres: 16/main: autovacuum launcher 
postgres    8622  0.0  0.0 224332  8860 ?        Ss   08:51   0:00 postgres: 16/main: logical replication launcher 
utcl        9372  0.0  0.0   6976  2048 pts/1    S+   08:54   0:00 grep --color=auto postgres

   # Login to PostgreSQL as the default user
sudo -u postgres psql

# Create a new database
CREATE DATABASE fleetmis;

# Create a new user
CREATE USER fleetuser WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE fleetmis TO fleetuser;

# Exit PostgreSQL
\q

# then Update settings.p:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# Ensure that you make some permision grantings to the the user:
sudo -u postgres psql
-- STEP 1: Connect to the database
\c fleetmis
# you should see something like this below:
You are now connected to database "fleetmis" as user "postgres".
-- STEP 2: Grant privileges on the schema
GRANT ALL ON SCHEMA public TO rasheed;

-- STEP 3: Optional but recommended: make rasheed the owner of the schema
ALTER SCHEMA public OWNER TO rasheed;

✅ Then:
Apply migrations:

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

# ToDo List Pendings  =============================================

  Some pending functionalities:
  * Need date should not allow passed dates, 
  * Modifications in reports
  * Emails to include need dates
  * Fleet Driver need date is missing
  ** ** Final Year Project report ** 

Role-based dashboard navigation (Manager vs User vs Driver)

New screens (TripRecords, RequestVehicle, etc.)

Data visualizations or backend optimizations

Deployment tips or security enhancements.

✅ Next Steps
Now that layouts are ready, here’s what follows:

1. 🔨 Activities to create:
RequestVehicleActivity.kt

TrackMyRequestsActivity.kt

AssignedTripsActivity.kt

TripHistoryActivity.kt

DriverProfileActivity.kt

Each will have a layout (XML) and optionally interact with the Django API.

2. ⚙ Django Backend
/api/driver/profile/

/api/requests/user/ → filter by user

/api/requests/driver/ → for drivers

/api/requests/create/ → create trip request

Shall I proceed creating the first two Activities with sample UI and connect to Django mock endpoints?


