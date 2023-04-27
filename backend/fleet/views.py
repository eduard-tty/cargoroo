from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Fleet, Bike
from .serializers import FleetSerializer, BikeSerializer

@api_view(['GET','POST','PUT','DELETE'])
def dispatch_on_method(request, *args, **kwargs):  # Why does drf not handle this?
    if request.method == "GET":
        return get_list_of_fleets(request, args, kwargs)
    elif request.method == "PUT":
        return create_a_fleet(request, args, kwargs)
    elif request.method == "POST":
        return update_a_fleet(request, args, kwargs)
    elif request.method == "DELETE":
        return delete_a_fleet(request, args, kwargs)
    else:
        raise "Unexpected http method: '{}'".format(request.method)
    

def get_list_of_fleets(request, *args, **kwargs):
    data = list(Fleet.objects.values())
    return JsonResponse( data, safe=False )


def create_a_fleet(request, *args, **kwargs):
    data = {
        'method' : 'PUT',
    }
    return JsonResponse( data )

def update_a_fleet(request, *args, **kwargs):
    data = {
        'method' : 'POST',
    }
    return JsonResponse( data )

def delete_a_fleet(request, *args, **kwargs):
    data = {
        'method' : 'DELETE',
    }
    return JsonResponse( data )


def show_fleet(request, id, *args, **kwargs):
    fleet = Fleet.objects.get(id=id)
    data = FleetSerializer(fleet).data
    return JsonResponse( data, safe=False ) #  Error handling