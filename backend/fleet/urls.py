from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from . import views

schema_view = swagger_get_schema_view(
    openapi.Info(
    title = 'Cargoroo REST API',
    default_version='1.0.0',
    description='Cargoroo fleet and bike REST API',
    ),
    public=True,
)

urlpatterns = [
    path('fleet/', views.list_fleets),
    path('fleet/<str:fid>', views.fleet_id_dispatch),
    path('fleet/<str:fid>/bike', views.list_bikes_in_fleet),
    path('bike/<str:bid>', views.bike_id_dispatch),
    path('docs/', include([
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger=schema')
    ])),
]
