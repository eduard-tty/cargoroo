from rest_framework import serializers
from .models import Fleet, Bike


class FleetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fleet
        fields = ['id', 'name']


class BikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bike
        fields = ['id', 'fleet', 'status', 'latitude', 'longitude']
