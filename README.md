# cargoroo

Cargo bike api

GET    http://localhost:8000/rest/v1/docs                   Show API documentation

GET    http://localhost:8000/rest/v1/fleet                  List all fleets
PUT    http://localhost:8000/rest/v1/fleet                  Create a new fleet
POST   http://localhost:8000/rest/v1/fleet/<id>             Update a fleet
DELETE http://localhost:8000/rest/v1/fleet/<id>             Delete a fleet (that has no bikes in it)

GET    http://localhost:8000/rest/v1/fleet/<id>/bike        List all bikes in fleet <id>
PUT    http://localhost:8000/rest/v1/fleet/<id>/bike        Create a new bike in fleet <id>
POST   http://localhost:8000/rest/v1/bike/<id>              Update bike <id> (move bikes between fleets)
DELETE http://localhost:8000/rest/v1/bike/<id>              Delete bike <id>

