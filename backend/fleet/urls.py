from django.urls import path
from . import views

urlpatterns = [
    path('',views.dispatch_on_method),
]