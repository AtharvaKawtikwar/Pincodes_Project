from rest_framework import serializers
from .models import NearbyPincode

class NearbyPincodeSerializer(serializers.ModelSerializer):
    nearby_pincode = serializers.JSONField()  # Make sure this field is serializable

    class Meta:
        model = NearbyPincode
        fields = ['base_pincode', 'nearby_pincode']
