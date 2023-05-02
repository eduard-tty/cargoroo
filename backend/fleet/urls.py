from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from . import views

schema_view = swagger_get_schema_view(
    openapi.Info(
        title='Cargoroo REST API',
        default_version='1.0.0',
        description='Cargoroo fleet and bike REST API',
    ),
    public=True,
)

urlpatterns = [
    path('fleet/', views.FleetList.as_view()),
    path('fleet/<str:fid>', views.FleetItem.as_view()),
    path('fleet/<str:fid>/bike', views.BikesInFleet.as_view()),
    path('bike/<str:bid>', views.BikeItem.as_view()),
    path('', schema_view.with_ui()),
]
