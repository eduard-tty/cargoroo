# cargoroo

Cargo bike API



# general

GET    http://localhost:8000/                               Show homepage
GET    http://localhost:8000/rest/v1/schema                 Show openapi schema
GET    http://localhost:8000/rest/v1/docs                   Show API documentation

# fleets

GET    http://localhost:8000/rest/v1/fleet                  List all fleets
GET    http://localhost:8000/rest/v1/fleet/<id>             Show fleet with id <id>
PUT    http://localhost:8000/rest/v1/fleet/<id>             Create a new fleet
POST   http://localhost:8000/rest/v1/fleet/<id>             Update a fleet
DELETE http://localhost:8000/rest/v1/fleet/<id>             Delete a fleet AND IT'S BIKES!

# bikes in fleets

GET    http://localhost:8000/rest/v1/fleet/<id>/bike        List all bikes in fleet <id>

# bikes

GET    http://localhost:8000/rest/v1/bike/<id>              Show bike with id <id>
PUT    http://localhost:8000/rest/v1/bike/<id>     e        Create a new bike in fleet
POST   http://localhost:8000/rest/v1/bike/<id>              Update bike <id> (move bikes between fleets)
DELETE http://localhost:8000/rest/v1/bike/<id>              Delete bike <id>




Out of scope:
- authetication
- hardening
- csrf

Inspiration: https://www.bezkoder.com/django-rest-api/

