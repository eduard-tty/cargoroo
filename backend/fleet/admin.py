from django.contrib import admin

from .models import Fleet, Bike

admin.site.register([
        Fleet, 
        Bike
    ]
) 