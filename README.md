# Project 42K-main

42K-main is a (short description) built with [Python][0] using the [Django Web Framework][1].

This project has the following basic apps:

* App1 (short desc)
* App2 (short desc)
* App3 (short desc)

## Installation

### Quick start

To set up a development environment quickly, first install Python 2.7.

Create a virtual env by:

    1. `$ virtualenv ../venv
    2. `$ source ../venv/bin/activate

Now the pip commands should work smoothly. Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate

### Facebook login

First create a Django superuser:

    python manage.py createsuperuser

Then start the testserver:

    python manage.py runserver
    
Go to <http://localhost:8000/admin/socialaccount/socialapp/add/>, 
choose the Provider 'Facebook' and enter the following values:

    Name: Facebook
    Client id: 1582734425306832
    Secret key: bc30440a1f440c296f1f60775883aac1
    
Now you can test the facebook login: <http://localhost:8000/accounts/login/>

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
