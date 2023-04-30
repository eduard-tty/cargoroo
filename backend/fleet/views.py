from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Fleet, Bike
from .serializers import FleetSerializer, BikeSerializer

## Fleets ##

@api_view(['GET'])
def list_fleets(request, *args, **kwargs):
    data = [ FleetSerializer(x).data for x in Fleet.objects.all() ]
    return JsonResponse( data, safe=False )

@api_view(['GET','POST','PUT', 'DELETE'])
def fleet_id_dispatch(request, id, *args, **kwargs):
    try:    
        if request.method == "GET":
            return show_fleet(request, id, args, kwargs)
        elif request.method == "POST":
            return create_a_fleet(request, id, args, kwargs)
        elif request.method == "PUT":
            return update_a_fleet(request, id, args, kwargs)
        elif request.method == "DELETE":
            return delete_a_fleet(request, id, args, kwargs)
        else:
            raise "Unexpected http method: '{}'".format(request.method)
    except:
        return Response('', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def show_fleet(request, id, *args, **kwargs):
    fleet = Fleet.objects.filter(id=id).first()
    if None == fleet:
        return Response('', status=status.HTTP_404_NOT_FOUND)
    else:
        data = FleetSerializer(fleet).data
        return JsonResponse(data, safe=False)


def create_a_fleet(request, id, *args, **kwargs):
    fleet = Fleet(id=id, name=request.POST['name'])
    fleet.save()
    data = FleetSerializer(fleet).data
    return JsonResponse(data)


def update_a_fleet(request, id, *args, **kwargs):
    fleet = Fleet.objects.filter(id=id).first()
    if None == fleet:
        return Response('', status=status.HTTP_404_NOT_FOUND)
    else:
        fleet.name = request.POST['name']
        fleet.save()
        data = FleetSerializer(fleet).data
        return JsonResponse(data)


def delete_a_fleet(request, id, *args, **kwargs):
    fleet = Fleet.objects.filter(id=id).first()
    if None == fleet:
        return Response('', status=status.HTTP_404_NOT_FOUND)
    else:
        data = FleetSerializer(fleet).data
        fleet.delete()
        return JsonResponse(data)    

@api_view(['GET'])
def list_bikes_in_fleet(request, id, *args, **kwargs):
    try:
        data = [ BikeSerializer(x).data for x in Bike.objects.filter(fleet=id).all() ]
        return JsonResponse( data, safe=False)
    except:
        return Response('', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## Bikes ##

@api_view(['GET','POST','PUT', 'DELETE'])
def bike_id_dispatch(request, id, *args, **kwargs):
    if request.method == "GET":
        return show_bike(request, id, args, kwargs)
    elif request.method == "POST":
        print('1')
        return create_a_bike(request, id, args, kwargs)
    elif request.method == "PUT":
        return update_a_bike(request, id, args, kwargs)
    elif request.method == "DELETE":
        return delete_a_bike(request, id, args, kwargs)
    else:
        raise "Unexpected http method: '{}'".format(request.method)

def show_bike(request, id, *args, **kwargs):
    bike = Bike.objects.filter(id=id).first()
    if None == bike:
        return Response('', status=status.HTTP_404_NOT_FOUND)
    else:
        data = BikeSerializer(bike).data
        return JsonResponse(data, safe=False)


def create_a_bike(request, id, *args, **kwargs):
    fleet_id = request.POST['fleet']
    fleet = Fleet.objects.filter(id=fleet_id).first()
    if None == fleet:
        error = "Fleet '{}' not found".format(fleet_id)
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    else:
        bike = Bike(id=id, fleet=fleet, status='unlocked')
        bike.save()
        data = BikeSerializer(bike).data
        return JsonResponse(data)


def update_a_bike(request, id, *args, **kwargs):
    fleet_id = request.POST['fleet']
    fleet = Fleet.objects.filter(id=fleet_id).first()
    if None == fleet:
        error = "Fleet '{}' not found".format(fleet_id)
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    else:
        bike = Bike.objects.filter(id=id).first()
        if None == bike:
            error = "Bike '{}' not found".format(id)
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        else:
            bike.fleet = fleet
            bike.status = request.POST['status']
            bike.save()
            data = BikeSerializer(bike).data
            return JsonResponse(data)


def delete_a_bike(request, id, *args, **kwargs):
    bike = Bike.objects.filter(id=id).first()
    if None == bike:
        error = "Bike '{}' not found".format(id)
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    else:
        data = BikeSerializer(bike).data
        bike.delete()
        return JsonResponse(data)    