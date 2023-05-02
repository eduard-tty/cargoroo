# Cargoroo REST API

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/eduard-tty/cargoroo.git
$ cd cargoroo
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd backend
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/rest/v1/`.


# DESIGN Notes

GET    http://localhost:8000/                               Show homepage
GET    http://localhost:8000/rest/v1/schema                 Show openapi schema
GET    http://localhost:8000/rest/v1/docs                   Show API documentation

# fleets

GET    http://localhost:8000/rest/v1/fleet                  List all fleets
GET    http://localhost:8000/rest/v1/fleet/<id>             Show fleet with id <id>
POST   http://localhost:8000/rest/v1/fleet/<id>             Create a new fleet
PUT    http://localhost:8000/rest/v1/fleet/<id>             Update a fleet
DELETE http://localhost:8000/rest/v1/fleet/<id>             Delete a fleet AND IT'S BIKES!

# bikes in fleets

GET    http://localhost:8000/rest/v1/fleet/<id>/bike        List all bikes in fleet <id>

# bikes

GET    http://localhost:8000/rest/v1/bike/<id>              Show bike with id <id>
POST   http://localhost:8000/rest/v1/bike/<id>              Create a new bike in fleet
PUT    http://localhost:8000/rest/v1/bike/<id>              Update bike <id> (move bikes between fleets)
DELETE http://localhost:8000/rest/v1/bike/<id>              Delete bike <id>
