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

And navigate to `http://127.0.0.1:8000/rest/v1/` for swagger docs.
