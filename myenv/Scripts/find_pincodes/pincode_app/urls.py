from django.urls import path
from .views import find_nearby_pincodes, home

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('find-nearby-pincodes/', find_nearby_pincodes, name='find_nearby_pincodes'),  # Can be called without pincode
    path('find-nearby-pincodes/<str:pincode>/', find_nearby_pincodes, name='find_nearby_pincodes_with_pincode'),  # With pincode
    path('api/nearby-pincodes/<str:pincode>/', find_nearby_pincodes, name='api_get_nearby_pincodes'),  # API for nearby pincodes
]
