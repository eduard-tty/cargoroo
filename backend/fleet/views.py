from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Fleet, Bike
from .serializers import FleetSerializer, BikeSerializer


@api_view(['GET'])
def list_fleets(request, *args, **kwargs):
    ''' Return a JSON list of all fleets. '''
    data = [FleetSerializer(x).data for x in Fleet.objects.all()]
    return JsonResponse(data, safe=False)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def fleet_id_dispatch(request, fid, *args, **kwargs):
    if request.method == "GET":
        return show_fleet(request, fid, args, kwargs) 
    if request.method == "POST":
        return create_a_fleet(request, fid, args, kwargs)
    if request.method == "PUT":
        return update_a_fleet(request, fid, args, kwargs)
    if request.method == "DELETE":
        return delete_a_fleet(request, fid, args, kwargs)
    error = f"Unexpected HTTP method '{request.method}'"
    return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def show_fleet(request, id, *args, **kwargs):
    ''' Show all details of a fleet. '''
    fleet = Fleet.objects.filter(id=id).first()
    if fleet is None:
        error = f"Fleet '{id}' not found"
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    data = FleetSerializer(fleet).data
    return JsonResponse(data, safe=False)


def create_a_fleet(request, id, *args, **kwargs):
    name = request.POST.get('name')
    if name is None:
    if name is None:
        error = "name was missing from post data"
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    fleet = Fleet(id=id, name=name)
    fleet.save()
    data = FleetSerializer(fleet).data
    return JsonResponse(data, status=status.HTTP_201_CREATED)


def update_a_fleet(request, id, *args, **kwargs):
    fleet = Fleet.objects.filter(id=id).first()
    if fleet is None:
        error = f"Fleet '{id}' not found"
    if fleet is None:
        error = f"Fleet '{id}' not found"
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    name = request.POST.get('name')
    if name is not None:
        fleet.name = name
    fleet.save()
    data = FleetSerializer(fleet).data
    return JsonResponse(data)


def delete_a_fleet(request, id, *args, **kwargs):
    fleet = Fleet.objects.filter(id=id).first()
    if None is fleet:
        error = f"Fleet '{id}' not found"
    if None is fleet:
        error = f"Fleet '{id}' not found"
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    data = FleetSerializer(fleet).data
    fleet.delete()
    return JsonResponse(data)


@api_view(['GET'])
def list_bikes_in_fleet(request, id, *args, **kwargs):
    fleet = Fleet.objects.filter(id=id).first()
    if fleet is None:
        error = f"Fleet '{id}' not found"
    if fleet is None:
        error = f"Fleet '{id}' not found"
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    try:
        data = [BikeSerializer(
            x).data for x in Bike.objects.filter(fleet=id).all()]
        return JsonResponse(data, safe=False)
    except:
        error = f"Error loading bikes for fleet '{id}'"
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## Bikes ##


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def bike_id_dispatch(request, id, *args, **kwargs):
    if request.method == "GET":
        return show_bike(request, id, args, kwargs)
    if request.method == "POST":
        return create_a_bike(request, id, args, kwargs)
    if request.method == "PUT":
        return update_a_bike(request, id, args, kwargs)
    if request.method == "DELETE":
        return delete_a_bike(request, id, args, kwargs)
    error = f"Unexpected HTTP method '{request.method}'"
    return Response(error, status=status.HTTP_404_NOT_FOUND)


def show_bike(request, id, *args, **kwargs):
    bike = Bike.objects.filter(id=id).first()
    if bike is None:
        error = f"Bike '{id}' not found"
    if bike is None:
        error = f"Bike '{id}' not found"
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    data = BikeSerializer(bike).data
    return JsonResponse(data, safe=False)


def create_a_bike(request, id, *args, **kwargs):
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
    except:
        error = f"Location format error in latitude '{lat}' and/or longitude '{long}' "
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    if bike_status not in ('locked', 'unlocked'):
        error = f"Illegal status '{bike_status}'"
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    bike = Bike(id=id, fleet=fleet, latitude=latitude,
                longitude=longitude, status=bike_status)
    bike.save()
    data = BikeSerializer(bike).data
    return JsonResponse(data, status=status.HTTP_201_CREATED)


def update_a_bike(request, id, *args, **kwargs):
    fleet_id = request.POST.get('fleet')
    lat = request.POST.get('latitude')
    long = request.POST.get('longitude')
    bike_status = request.POST.get('status')
    fleet = Fleet.objects.filter(id=fleet_id).first()
    if fleet is None:
        error = f"Fleet '{fleet_id}' not found"
    if fleet is None:
        error = f"Fleet '{fleet_id}' not found"
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    bike = Bike.objects.filter(id=id).first()
    if bike is None:
        error = f"Bike '{id}' not found"
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    try:
        latitude = float(lat)
        longitude = float(long)
    except:
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


def delete_a_bike(request, id, *args, **kwargs):
    bike = Bike.objects.filter(id=id).first()
    if bike is None:
        error = f"Bike '{id}' not found"
    if bike is None:
        error = f"Bike '{id}' not found"
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    data = BikeSerializer(bike).data
    bike.delete()
    return JsonResponse(data)
