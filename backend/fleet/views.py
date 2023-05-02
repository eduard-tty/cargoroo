from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Fleet, Bike
from .serializers import FleetSerializer, BikeSerializer

class FleetList(APIView):

    def get(self, request, *args, **kwargs):
        data = [FleetSerializer(x).data for x in Fleet.objects.all()]
        return JsonResponse(data, safe=False)

class FleetItem(APIView):

    def get(self, request, fid, *args, **kwargs):
        fleet = Fleet.objects.filter(id=fid).first()
        if fleet is None:
            error = f"Fleet '{fid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = FleetSerializer(fleet).data
        return JsonResponse(data, safe=False)


    def post(self, request, fid, *args, **kwargs):
        name = request.POST.get('name')
        if name is None:
            error = "name was missing from post data"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        fleet = Fleet(id=fid, name=name)
        fleet.save()
        data = FleetSerializer(fleet).data
        return JsonResponse(data, status=status.HTTP_201_CREATED)


    def put(self, request, fid, *args, **kwargs):
        fleet = Fleet.objects.filter(id=fid).first()
        if fleet is None:
            error = f"Fleet '{fid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        name = request.POST.get('name')
        if name is not None:
            fleet.name = name
        fleet.save()
        data = FleetSerializer(fleet).data
        return JsonResponse(data)


    def delete(self, request, fid, *args, **kwargs):
        fleet = Fleet.objects.filter(id=fid).first()
        if fleet is None:
            error = f"Fleet '{fid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = FleetSerializer(fleet).data
        fleet.delete()
        return JsonResponse(data)

class BikesInFleet(APIView):

    def get(self, request, fid, *args, **kwargs):
        fleet = Fleet.objects.filter(id=fid).first()
        if fleet is None:
            error = f"Fleet '{fid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = [BikeSerializer(x).data for x in Bike.objects.filter(fleet=fid).all()]
        return JsonResponse(data, safe=False)

class BikeItem(APIView):

    def get(self, request, bid, *args, **kwargs):
        bike = Bike.objects.filter(id=bid).first()
        if bike is None:
            error = f"Bike '{bid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = BikeSerializer(bike).data
        return JsonResponse(data, safe=False)


    def post(self, request, bid, *args, **kwargs):
        fleet_id = request.POST.get('fleet')
        bike_status = request.POST.get('status')
        fleet = Fleet.objects.filter(id=fleet_id).first()
        if fleet is None:
            error = f"Fleet '{fleet_id}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        lat = request.POST.get('latitude')
        long = request.POST.get('longitude')
        try:
            latitude = float(lat)
            longitude = float(long)
        except NameError:
            error = f"Location format error in latitude '{lat}' and/or longitude '{long}' "
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if bike_status not in ('locked', 'unlocked'):
            error = f"Illegal status '{bike_status}'"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        bike = Bike(
            id=bid,
            fleet=fleet,
            latitude=latitude,
            longitude=longitude,
            status=bike_status,
        )
        bike.save()
        data = BikeSerializer(bike).data
        return JsonResponse(data, status=status.HTTP_201_CREATED)


    def put(self, request, bid, *args, **kwargs):
        fleet_id = request.POST.get('fleet')
        lat = request.POST.get('latitude')
        long = request.POST.get('longitude')
        bike_status = request.POST.get('status')
        fleet = Fleet.objects.filter(id=fleet_id).first()
        if fleet is None:
            error = f"Fleet '{fleet_id}' not found"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        bike = Bike.objects.filter(id=bid).first()
        if bike is None:
            error = f"Bike '{bid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        try:
            latitude = float(lat)
            longitude = float(long)
        except ValueError:
            error = f"Location format error in latitude '{lat}' and/or longitude '{long}' "
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        bike.fleet = fleet
        if bike_status in ('locked', 'unlocked'):
            bike.status = bike_status
        else:
            error = f"Illegal status '{status}'"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        bike.latitude = latitude
        bike.longitude = longitude
        bike.save()
        data = BikeSerializer(bike).data
        return JsonResponse(data)


    def delete(self, request, bid, *args, **kwargs):
        bike = Bike.objects.filter(id=bid).first()
        if bike is None:
            error = f"Bike '{bid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = BikeSerializer(bike).data
        bike.delete()
        return JsonResponse(data)
