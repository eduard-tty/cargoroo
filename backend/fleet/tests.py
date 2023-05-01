import io
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.parsers import JSONParser
from .models import Fleet, Bike

class FleetTestCase(APITestCase):

    AMSTERDAM_LAT  = 52.377956
    AMSTERDAM_LONG = 4.897070

    def setUp(self):
        fleet1 = Fleet.objects.create(id='FL_001', name = 'Fleet one')
        Bike.objects.create(id='BK_001', fleet = fleet1, status = 'unlocked', latitude=self.AMSTERDAM_LAT, longitude=self.AMSTERDAM_LONG)
        Bike.objects.create(id='BK_002', fleet = fleet1, status = 'locked', latitude=self.AMSTERDAM_LAT, longitude=self.AMSTERDAM_LONG)
        fleet2 = Fleet.objects.create(id='FL_002', name = 'Fleet two')
        Bike.objects.create(id='BK_003', fleet = fleet2, status = 'unlocked', latitude=self.AMSTERDAM_LAT, longitude=self.AMSTERDAM_LONG)
        

    def test_list_fleets(self):
        url = '/rest/v1/fleet/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Returns OK')
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(data[0]['id'], 'FL_001')
        self.assertEqual(data[0]['name'], 'Fleet one')
        self.assertEqual(data[1]['id'], 'FL_002')
        self.assertEqual(data[1]['name'], 'Fleet two')

    def test_create_fleet(self):
        id = 'FL_999'
        name = 'Automated Testing Fleet 999'
        url = "/rest/v1/fleet/{}".format(id)
        fleet_data = { 'name' : name }
        response = self.client.post(url, data=fleet_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Returns CREATED')
        self.assertEqual(3, Fleet.objects.count(), 'Has 3 fleets')
        fleet999 = Fleet.objects.filter(id=id).first()
        self.assertEqual(fleet999.id, id, 'Fleet id unchaged')
        self.assertEqual(fleet999.name, name, 'Fleet name updated')
        
    def test_show_a_fleet(self):
        fid = 'FL_001'
        url = "/rest/v1/fleet/{}".format(fid)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Returns OK')
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(data['id'], 'FL_001')
        self.assertEqual(data['name'], 'Fleet one')

    def test_update_a_fleet(self):
        fid = 'FL_001'
        name = 'Updated name'
        url = "/rest/v1/fleet/{}".format(fid)
        fleet_data = { 'name' : name }
        response = self.client.put(url, data=fleet_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Returns OK')
        fleet1 = Fleet.objects.filter(id=fid).first()
        self.assertEqual(fleet1.id, fid, "Id is unchaged")
        self.assertEqual(fleet1.name, name, "Name is updated")


    def test_delete_a_fleet(self):
        fid = 'FL_001'
        url = "/rest/v1/fleet/{}".format(fid)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Returns OK')
        fleet1 = Fleet.objects.filter(id=fid).first()
        self.assertEqual(fleet1, None)
        # Return deleted data in response
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(data['id'], 'FL_001')
        self.assertEqual(data['name'], 'Fleet one')

    def test_list_bikes_in_fleet(self):
        bid = 'FL_001'
        url = "/rest/v1/fleet/{}/bike".format(bid)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Returns OK')
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(2, len(data), 'returns 2 bikes')


    def test_create_bike(self):
        bid = 'BK_999'
        fid = 'FL_001'
        url = "/rest/v1/bike/{}".format(bid)
        bike_data = { 
            'fleet': fid,
            'status': 'locked',
            'latitude' : self.AMSTERDAM_LAT,
            'longitude' : self.AMSTERDAM_LONG,
        }
        response = self.client.post(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Returns CREATED')
        bike999 = Bike.objects.filter(id=bid).first()
        self.assertEqual(bike999.id, bid)
        self.assertEqual(bike999.fleet.id, fid)
        self.assertEqual(bike999.status, 'locked')
        self.assertEqual(bike999.latitude, self.AMSTERDAM_LAT)
        self.assertEqual(bike999.longitude, self.AMSTERDAM_LONG)
        
    def test_show_a_bike(self):
        bid = 'BK_003'
        url = "/rest/v1/bike/{}".format(bid)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Returns OK')
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(data['id'], bid)
        self.assertEqual(data['fleet'], 'FL_002')
        self.assertEqual(data['status'], 'unlocked')
        self.assertEqual(data['latitude'], self.AMSTERDAM_LAT)
        self.assertEqual(data['longitude'], self.AMSTERDAM_LONG)      

    def test_update_a_bike(self):
        bid = 'BK_003'
        fid = 'FL_002'
        url = "/rest/v1/bike/{}".format(bid)
        bike_data = { 
            'fleet': fid,
            'status': 'locked',
            'latitude' : 1.0,
            'longitude' : 1.0,
        }
        response = self.client.put(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Returns OK')
        bike1 = Bike.objects.filter(id=bid).first()
        self.assertEqual(bike1.id, bid, "Id is unchaged")
        self.assertEqual(bike1.fleet.id, fid)
        self.assertEqual(bike1.status, 'locked')
        self.assertEqual(bike1.latitude, 1.0)
        self.assertEqual(bike1.longitude, 1.0)
        

    def test_delete_a_bike(self):
        bid = 'BK_001'
        url = "/rest/v1/bike/{}".format(bid)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Returns OK')
        self.assertEqual(Fleet.objects.filter(id=bid).first(), None, 'Bike is gone')
        # Return deleted data in response
        data = JSONParser().parse(io.BytesIO(response.content))
        self.assertEqual(data['id'], bid)
        self.assertEqual(data['fleet'], 'FL_001')
        self.assertEqual(data['status'], 'unlocked')
        self.assertEqual(data['latitude'], self.AMSTERDAM_LAT)
        self.assertEqual(data['longitude'], self.AMSTERDAM_LONG)
        
        
class ErrorTestCase(APITestCase):

    AMSTERDAM_LAT  = 52.377956
    AMSTERDAM_LONG = 4.897070

    def setUp(self):
        fleet1 = Fleet.objects.create(id='FL_001', name = 'Fleet one')
        Bike.objects.create(id='BK_001', fleet = fleet1, status = 'unlocked', latitude=self.AMSTERDAM_LAT, longitude=self.AMSTERDAM_LONG)
        Bike.objects.create(id='BK_002', fleet = fleet1, status = 'locked', latitude=self.AMSTERDAM_LAT, longitude=self.AMSTERDAM_LONG)
        fleet2 = Fleet.objects.create(id='FL_002', name = 'Fleet two')
        Bike.objects.create(id='BK_003', fleet = fleet2, status = 'unlocked', latitude=self.AMSTERDAM_LAT, longitude=self.AMSTERDAM_LONG)
        

    def test_list_fleets(self):
        url = '/rest/v1/car/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = '/rest/v2/fleet/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = '/rest/fleet/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = '/test/v1/fleet/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_sleet(self):
        url = '/test/v1/fleet/not_a_fleet'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_fleet(self):
        fid = 'FL_999'
        name = 'Automated Testing Fleet 999'
        url = "/rest/v1/fleet/{}".format(fid)
        fleet_data = { 
            'title' : name,
        }
        response = self.client.post(url, data=fleet_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
  
   
    def test_update_a_fleet(self):
        url = f"/rest/v1/fleet/no_id"
        bike_data = { 
            'name' : 'Fleet name',
        }
        response = self.client.put(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
      
    def test_delete_a_fleet(self):
        url = '/rest/v1/fleet/no_id'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_bike(self):
        bid = 'BK_999'
        fid = 'FL_001'
        url = f"/rest/v1/bike/{bid}"
        bike_data = { 
            'fleet': fid,
            'status': 'blue',
            'latitude' : self.AMSTERDAM_LAT,
            'longitude' : self.AMSTERDAM_LONG,
        }
        response = self.client.post(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_update_a_bike(self):
        bid = 'BK_003'
        fid = 'FL_002'
        url = f"/rest/v1/bike/{bid}"
        bike_data = { 
            'xxxx': fid,
            'status': 'locked',
            'latitude' : 1.0,
            'longitude' : 1.0,
        }
        response = self.client.put(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        bike_data['fleet'] = fid
        bike_data['latitude'] = 'boo'
        response = self.client.put(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      
        bike_data['latitude'] = 1.0
        bike_data['status'] = 'blue'
        response = self.client.put(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        bike_data['status'] = 'locked'  
        url = '/rest/v1/bike/no_id'
        response = self.client.put(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
  
        
    def test_delete_a_bike(self):
        url = '/rest/v1/bike/no_id'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
