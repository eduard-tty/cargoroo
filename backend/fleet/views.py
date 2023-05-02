from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import FleetSerializer, BikeSerializer
from .models import Fleet, Bike


class FleetList(APIView):

    @swagger_auto_schema(
        operation_summary='List all fleets',
        operation_description='List all fleets.',
    )
    def get(self, request, *args, **kwargs):
        data = [FleetSerializer(x).data for x in Fleet.objects.all()]
        return JsonResponse(data, safe=False)

class FleetItem(APIView):

    @swagger_auto_schema(
        operation_summary='Fleet details',
        operation_description='List fields for a given fleet.',
    )
    def get(self, request, fid, *args, **kwargs):
        fleet = Fleet.objects.filter(id=fid).first()
        if fleet is None:
            error = f"Fleet '{fid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = FleetSerializer(fleet).data
        return JsonResponse(data, safe=False)

    @swagger_auto_schema(
        operation_summary='Create a fleet',
        operation_description='Creater a new Fleet object',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name' : openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def post(self, request, fid, *args, **kwargs):
        name = request.data.get('name')
        if name is None:
            error = "name was missing from post data"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        fleet = Fleet(id=fid, name=name)
        fleet.save()
        data = FleetSerializer(fleet).data
        return JsonResponse(data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(
        operation_summary='Update a fleet',
        operation_description='Update the fields of a fleet.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name' : openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def put(self, request, fid, *args, **kwargs):
        fleet = Fleet.objects.filter(id=fid).first()
        if fleet is None:
            error = f"Fleet '{fid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        name = request.data.get('name')
        if name is not None:
            fleet.name = name
        fleet.save()
        data = FleetSerializer(fleet).data
        return JsonResponse(data)


    @swagger_auto_schema(
        operation_summary='Delete a fleet (including all it\'s bikes!)',
        operation_description='Delete the given fleet. THIS DELETES ALL BIKES IN THAT FLEET!',
    )
    def delete(self, request, fid, *args, **kwargs):
        fleet = Fleet.objects.filter(id=fid).first()
        if fleet is None:
            error = f"Fleet '{fid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = FleetSerializer(fleet).data
        fleet.delete()
        return JsonResponse(data)

class BikesInFleet(APIView):

    @swagger_auto_schema(
        operation_summary='List bikes by fleet',
        operation_description='List all bikes in a given fleet.',
    )
    def get(self, request, fid, *args, **kwargs):
        fleet = Fleet.objects.filter(id=fid).first()
        if fleet is None:
            error = f"Fleet '{fid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = [BikeSerializer(x).data for x in Bike.objects.filter(fleet=fid).all()]
        return JsonResponse(data, safe=False)

class BikeItem(APIView):

    @swagger_auto_schema(
        operation_summary='Bike details',
        operation_description='List fields for a given bike.',
    )
    def get(self, request, bid, *args, **kwargs):
        bike = Bike.objects.filter(id=bid).first()
        if bike is None:
            error = f"Bike '{bid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = BikeSerializer(bike).data
        return JsonResponse(data, safe=False)

    @swagger_auto_schema(
        operation_summary='Create a bike',
        operation_description='Creater a new Bike object.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['fleet', 'status', 'latitude', 'longitude'],
            properties={
                'fleet' : openapi.Schema(type=openapi.TYPE_STRING),
                'status' : openapi.Schema(type=openapi.TYPE_STRING),
                'latitude' : openapi.Schema(type=openapi.TYPE_NUMBER),
                'longitude' : openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        )
    )
    def post(self, request, bid, *args, **kwargs):
        fleet_id = request.data.get('fleet')
        bike_status = request.data.get('status')
        fleet = Fleet.objects.filter(id=fleet_id).first()
        if fleet is None:
            error = f"Fleet '{fleet_id}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
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

    @swagger_auto_schema(
        operation_summary='Update a bike',
        operation_description='Update an existing Bike object.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['fleet', 'status', 'latitude', 'longitude'],
            properties={
                'fleet' : openapi.Schema(type=openapi.TYPE_STRING),   #TODO Foreign key
                'status' : openapi.Schema(type=openapi.TYPE_STRING),  # TODO smehow enum
                'latitude' : openapi.Schema(type=openapi.TYPE_NUMBER),
                'longitude' : openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        )
    )
    def put(self, request, bid, *args, **kwargs):
        fleet_id = request.data.get('fleet')
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        bike_status = request.data.get('status')
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

    @swagger_auto_schema(
        operation_summary='Delete a bike',
        operation_description='Delete a Bike Object.',
    )
    def delete(self, request, bid, *args, **kwargs):
        bike = Bike.objects.filter(id=bid).first()
        if bike is None:
            error = f"Bike '{bid}' not found"
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        data = BikeSerializer(bike).data
        bike.delete()
        return JsonResponse(data)
