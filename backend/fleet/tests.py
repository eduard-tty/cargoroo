from rest_framework import status
from rest_framework.test import APITestCase
from .models import Fleet, Bike
from .serializers import FleetSerializer, BikeSerializer
import io
from rest_framework.parsers import JSONParser

class FleetTestCase(APITestCase):


    def setUp(self):
        Fleet.objects.create(id='FL_001', name = 'Fleet one')
        Fleet.objects.create(id='FL_002', name = 'Fleet two')
        

    def test_list_fleets(self):
        url = 'http://localhost:8000/rest/v1/fleet/'
        response = self.client.get(url, folow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(data[0]['id'], 'FL_001')
        self.assertEqual(data[0]['name'], 'Fleet one')
        self.assertEqual(data[1]['id'], 'FL_002')
        self.assertEqual(data[1]['name'], 'Fleet two')

    def test_create_fleet(self):
        id = 'FL_999'
        name = 'Automated Testing Fleet 999'
        url = "http://localhost:8000/rest/v1/fleet/{}".format(id)
        fleet_data = { 'name' : name }
        response = self.client.post(url, data=fleet_data, folow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Fleet.objects.count())
        fleet999 = Fleet.objects.filter(id=id).first()
        self.assertEqual(fleet999.id, id)
        self.assertEqual(fleet999.name, name)
        
    def test_show_a_fleet(self):
        id = 'FL_001'
        url = "http://localhost:8000/rest/v1/fleet/{}".format(id)
        response = self.client.get(url, folow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(data['id'], 'FL_001')
        self.assertEqual(data['name'], 'Fleet one')

    def test_update_a_fleet(self):
        id = 'FL_001'
        name = 'Updated name'
        url = "http://localhost:8000/rest/v1/fleet/{}".format(id)
        fleet_data = { 'name' : name }
        response = self.client.put(url, data=fleet_data, folow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fleet1 = Fleet.objects.filter(id=id).first()
        self.assertEqual(fleet1.id, id, "Id is unchaged")
        self.assertEqual(fleet1.name, name, "Name is updated")


    def test_delete_a_fleet(self):
        id = 'FL_001'
        url = "http://localhost:8000/rest/v1/fleet/{}".format(id)
        response = self.client.delete(url, folow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fleet1 = Fleet.objects.filter(id=id).first()
        self.assertEqual(fleet1, None)
        # Return deleted data in response
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(data['id'], 'FL_001')
        self.assertEqual(data['name'], 'Fleet one')

