# test-dashboard
poc test dashboard

### Installation & Setup
*** Virtual env
'pip install virtualenv'
run: 'virtualenv env'
activate: 'env\scripts\activate'
deactivate: 'env\scripts\deactivate'

*** Install django
'pip install django'

* check django command
'django-admin'  

* Create project
'django-admin startproject projectname'         #replace 'projectname' with anyname

""" Inside the project can have many apps """
* Create app
'python manange.py startapp base'        #can replace 'base' with anyname

* Install django REST framework
'pip install djangorestframework'


* Run this command after create API object or Database
python manage.py makemigrations
python manage.py migrate
