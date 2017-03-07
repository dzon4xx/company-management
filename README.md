# Company management REST API

## Description

This is api suitable for management of employees in small company. It allows you to
perform operations on employees:
- view 
- add 
- delete 
- filter 
- update

Every employee has also related profession which you can only view.

# Deployment

Application was developed using:
 - Python 3.5 
 - Django 1.10.5 
 - Django Rest Framework 3.5.4.

In order to deploy server hosting api you should:
- Got to application root folder
- Install python dependancies preferably in python virtual enviroment 
([virtualenv tut](http://docs.python-guide.org/en/latest/dev/virtualenvs/)) with: `pip install -r requirements.txt`
- Run application on django developement server with: `python manage.py runserver`

# Usage

Django rest framework supports browseable api so just go to `localhost:8000/` and you will see root of API.
You need to log in to see anything else than root view. Test user is already created. Click login in top right corner
and pass credentials.

```
user name = test
password = test
```

API is hiperlinked so feel free to explore it.
You can see the structure of API on `localhost:8000/docs/`.

Database is prepopulated with 20 randomly generated users - check `employees/scripts` directory. If you want 
to regenerate users: `bash setup.db` 

To filter employees by name, last_name or email send GET to: `localhost:8000/employees/?filter=<name|last_name|email>&value=<string to search>`, example: `http://localhost:8000/employees/?filter=email;value=gmail`

To create new employee POST json describing user to: `http://localhost:8000/employees/` example:
 
```
{
    "email": "braintri@gmail.com",
    "last_name": "New",
    "name": "Employee",
    "profession": "http://localhost:8000/professions/1/"
}
```
 
 To update employee name, last_name or profession POST json to: `http://localhost:8000/employees/<employee_email>/` 
 example:
 
 `POST to http://localhost:8000/employees/braintri@gmail.com`
 
  ```
{        
    "last_name": "Old",
    "name": "CoWorker",        
}
 ```
 
 # Tests
 
 Application has got integration tests of API. Check `employees/tests.py` To run tests: `python manage.py test`
 