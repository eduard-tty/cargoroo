from django.db import models

class Fleet(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Bike(models.Model):

    LOCKED = "locked"
    UNLOCKED = "unlocked"
    FIELD_CHOICES = (
        (LOCKED, LOCKED),
        (UNLOCKED, UNLOCKED),
    )

    id = models.CharField(max_length=6, primary_key=True)
    fleet = models.ForeignKey(Fleet,on_delete=models.CASCADE)  # Be careful deleting fleets or remove CASCADE
    status = models.CharField(max_length=12, null=False, blank=False, choices=FIELD_CHOICES, default=UNLOCKED)
    latitude = models.FloatField(max_length=20, null=False, blank=False)
    longitude = models.FloatField(max_length=20, null=False, blank=False)

    
    def __str__(self):
        return self.id