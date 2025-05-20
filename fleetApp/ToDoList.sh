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
sudo apt install python3 python3-pip python3-venv -y
python --version       # Or python3 --version on Linux
pip --version          # Or pip3 --version on Linux
python -m pip install --upgrade pip

python manage.py runserver

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
