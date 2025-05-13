✅ ================== 5. Optional Features to Add Later =============================

✅ Mileage Calculations. 

✅ Totals in services offered. 

✅  Email/SMS Notifications to fleet Manager, Driver, and Requestor
 i.e:
 * Driver is notified when a car is allocated, when a request for trip is assigned etc, 
 * Manager is notified when a car is returned, when there is a pending request for approval etc, 
 * Requestor is notified when a car is allocated for trip etc
 and other required or necessary notifications to respective individuals in the system. 

✅  Export reports all trip logs with alert summaries and all other required info in (CSV, PDF) for Printing reports. 


Chart views (speed trends, fuel drop, etc.)


Final Project report. 



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
   5 pip install crispy bootstrap4
   6 pip install django-crispy-forms crispy-bootstrap4
   7 pip install djangorestframework
   8 python manage.py runserver
   9 python installation
  

  Tab  driverphoto