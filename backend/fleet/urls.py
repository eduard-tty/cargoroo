from django.urls import path
from . import views

urlpatterns = [
    path('fleet/', views.list_fleets),
    path('fleet/<str:fid>', views.fleet_id_dispatch),
    path('fleet/<str:fid>/bike', views.list_bikes_in_fleet),
    path('bike/<str:bid>', views.bike_id_dispatch),
]
