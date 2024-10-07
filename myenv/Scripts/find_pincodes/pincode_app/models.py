from django.db import models
import json

class Pincode(models.Model):
    pincode = models.CharField(max_length=10, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    state_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.pincode} - {self.state_name}'

class NearbyPincode(models.Model):
    base_pincode = models.ForeignKey(Pincode, on_delete=models.CASCADE)
    nearby_pincode = models.JSONField(null=True)

    def __str__(self):
        # Convert the base pincode to a string and nearby_pincode to a dict for JSON serialization
        return f'{self.base_pincode} -> {json.dumps(self.nearby_pincode)}'
