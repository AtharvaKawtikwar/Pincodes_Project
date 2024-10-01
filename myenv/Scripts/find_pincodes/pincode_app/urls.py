# pincode_app/urls.py

from django.urls import path
from .views import find_nearby_pincodes  # Import only the existing view

urlpatterns = [
    path('find-nearby-pincodes/', find_nearby_pincodes, name='find_nearby_pincodes'),
    path('', find_nearby_pincodes, name='home'),  # Optionally use find_nearby_pincodes as default view
]
