from django.urls import path
from . import views

urlpatterns = [
    path('fleet/',views.list_fleets),
    path('fleet/<str:id>', views.fleet_id_dispatch),
    path('fleet/<str:id>/bike', views.list_bikes_in_fleet),
    path('bike/<str:id>', views.bike_id_dispatch),
 ]