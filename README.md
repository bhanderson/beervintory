# beervintory
Inventory for Beer!

#Intro
This project is just a simple website originally written in flask (1.0) now using django to track beer kegs and let people view what is on tap currently.

#How to run
```
pipenv sync
cd beervintory
python manage.py makemigrations {inventory,rate,request,website,api}
python manage.py migrate
python manage.py createsuperuser # fill out fields
python manage.py runserver
```
