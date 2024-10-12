# import math
# from django.shortcuts import get_object_or_404
# from django.http import Http404, JsonResponse
# from .models import NearbyPincode, Pincode
# from django.shortcuts import render, redirect

# def home(request):
#     default_pincode = '400706.0'  
#     return redirect('find_nearby_pincodes_with_pincode', pincode=default_pincode)

# def haversine(lat1, lon1, lat2, lon2):
#     """Haversine formula to calculate distance between two points on Earth."""
#     R = 6371 
#     dlat = math.radians(lat2 - lat1)
#     dlon = math.radians(lon2 - lon1)
#     a = (math.sin(dlat / 2) ** 2 +
#          math.cos(math.radians(lat1)) *
#          math.cos(math.radians(lat2)) *
#          math.sin(dlon / 2) ** 2)
#     c = 2 * math.asin(math.sqrt(a))
#     return R * c


# def get_neighboring_states(state_name):
#     """Return a list of neighboring states and union territories based on the given state name."""
#     neighbors = {
#         'Andaman & Nicobar Islands': [],
#         'Andhra Pradesh': ['Telangana', 'Tamil Nadu', 'Karnataka', 'Odisha', 'Chhattisgarh'],
#         'Arunachal Pradesh': ['Assam', 'Nagaland'],
#         'Assam': ['Arunachal Pradesh', 'Nagaland', 'Manipur', 'Mizoram', 'West Bengal', 'Meghalaya', 'Tripura'],
#         'Bihar': ['Uttar Pradesh', 'Jharkhand', 'West Bengal'],
#         'Chhattisgarh': ['Madhya Pradesh', 'Odisha', 'Jharkhand', 'Telangana', 'Maharashtra', 'Andhra Pradesh', 'Uttar Pradesh'],
#         'Dadra & Nagar Haveli': ['Gujarat', 'Maharashtra'],
#         'Daman & Diu': ['Gujarat', 'Maharashtra'],
#         'Delhi': ['Haryana', 'Uttar Pradesh'],
#         'Goa': ['Maharashtra', 'Karnataka'],
#         'Gujarat': ['Maharashtra', 'Rajasthan', 'Dadra & Nagar Haveli', 'Daman & Diu', 'Madhya Pradesh'],
#         'Haryana': ['Punjab', 'Himachal Pradesh', 'Delhi', 'Uttar Pradesh', 'Rajasthan', 'Chandigarh', 'Uttarakhand'],
#         'Himachal Pradesh': ['Jammu & Kashmir', 'Punjab', 'Uttarakhand', 'Haryana', 'Chandigarh', 'Uttar Pradesh'],
#         'Jammu & Kashmir': ['Himachal Pradesh', 'Punjab'],
#         'Jharkhand': ['Bihar', 'Uttar Pradesh', 'Chhattisgarh', 'West Bengal', 'Odisha'],
#         'Karnataka': ['Maharashtra', 'Goa', 'Andhra Pradesh', 'Tamil Nadu', 'Telangana', 'Kerala'],
#         'Kerala': ['Karnataka', 'Tamil Nadu'],
#         'Lakshadweep': [],
#         'Madhya Pradesh': ['Rajasthan', 'Uttar Pradesh', 'Chhattisgarh', 'Gujarat', 'Maharashtra'],
#         'Maharashtra': ['Gujarat', 'Madhya Pradesh', 'Chhattisgarh', 'Goa', 'Karnataka', 'Telangana', 'Daman & Diu', 'Dadra & Nagar Haveli'],
#         'Manipur': ['Nagaland', 'Mizoram', 'Assam'],
#         'Meghalaya': ['Assam'],
#         'Mizoram': ['Assam', 'Manipur', 'Tripura'],
#         'Nagaland': ['Arunachal Pradesh', 'Manipur', 'Assam'],
#         'Odisha': ['West Bengal', 'Jharkhand', 'Chhattisgarh', 'Andhra Pradesh'],
#         "Puducherry": ["Tamil Nadu"],
#         "Punjab": ["Haryana", "Himachal Pradesh", "Jammu & Kashmir", 'Chandigarh', 'Rajasthan'],
#         "Rajasthan": ["Punjab", "Haryana", "Uttar Pradesh", "Gujarat", "Madhya Pradesh", "Haryana"],
#         "Sikkim": ["West Bengal"],
#         "Tamil Nadu": ["Kerala", "Karnataka", "Andhra Pradesh", "Puducherry"],
#         "Telangana": ["Maharashtra", "Andhra Pradesh", "Karnataka", "Chhattisgarh"],
#         "Tripura": ["Assam", "Mizoram"],
#         "Uttar Pradesh": ["Uttarakhand", "Himachal Pradesh", "Haryana", "Delhi", "Rajasthan", "Bihar", "Jharkhand", "Madhya Pradesh", "Chhattisgarh"],
#         "Uttarakhand": ["Himachal Pradesh", "Uttar Pradesh", "Haryana"],
#         "West Bengal": ["Sikkim", "Assam", "Jharkhand", "Odisha", "Bihar"],
#     }

#     return neighbors.get(state_name, [])


# def find_nearby_pincodes(request, pincode=None):
#     """
#     API view to get nearby pincodes and distances based on the input pincode.
#     """
#     if pincode is None:
#         return JsonResponse({'error': 'Pincode is required.'}, status=400)

#     if request.method == 'GET':
       
#         try:
#             user_location = get_object_or_404(Pincode, pincode=pincode)
#         except Http404:
#             return JsonResponse({'error': 'No Pincode matches the given query.'}, status=404)

#         state_name = user_location.state_name

        
#         nearby_pincodes = Pincode.objects.filter(state_name=state_name)

#         neighboring_states = get_neighboring_states(state_name)
#         if neighboring_states:
#             nearby_pincodes = nearby_pincodes | Pincode.objects.filter(state_name__in=neighboring_states)

#         # Calculate distance and filter based on a threshold (10 km here)
#         nearby_list = []
#         for pincode_obj in nearby_pincodes:
#             distance = haversine(user_location.latitude, user_location.longitude,
#                                  pincode_obj.latitude, pincode_obj.longitude)

#             if distance <= 10 and pincode_obj.pincode != pincode:
#                 nearby_list.append({
#                     'pincode': pincode_obj.pincode,
#                     'distance': round(distance, 2),
#                 })

#                 NearbyPincode.objects.update_or_create(
#                     base_pincode=user_location,
#                     nearby_pincode=pincode_obj.pincode,
#                     defaults={
#                         'latitude': pincode_obj.latitude,
#                         'longitude': pincode_obj.longitude,
#                     }
#                 )

#         nearby_list.sort(key=lambda x: x['distance'])
#         result = nearby_list[:10]

#         return JsonResponse(result, safe=False)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)



import math
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from .models import Pincode
from django.shortcuts import render, redirect

def home(request):
    default_pincode = '400706.0'  # This may need to be adjusted for the correct format of pincode
    return redirect('find_nearby_pincodes_with_pincode', pincode=default_pincode)

def haversine(lat1, lon1, lat2, lon2):
    """Haversine formula to calculate distance between two points on Earth."""
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def get_neighboring_states(state_name):
#     """Return a list of neighboring states and union territories based on the given state name."""
    neighbors = {
        'Andaman & Nicobar Islands': [],
        'Andhra Pradesh': ['Telangana', 'Tamil Nadu', 'Karnataka', 'Odisha', 'Chhattisgarh'],
        'Arunachal Pradesh': ['Assam', 'Nagaland'],
        'Assam': ['Arunachal Pradesh', 'Nagaland', 'Manipur', 'Mizoram', 'West Bengal', 'Meghalaya', 'Tripura'],
        'Bihar': ['Uttar Pradesh', 'Jharkhand', 'West Bengal'],
        'Chhattisgarh': ['Madhya Pradesh', 'Odisha', 'Jharkhand', 'Telangana', 'Maharashtra', 'Andhra Pradesh', 'Uttar Pradesh'],
        'Dadra & Nagar Haveli': ['Gujarat', 'Maharashtra'],
        'Daman & Diu': ['Gujarat', 'Maharashtra'],
        'Delhi': ['Haryana', 'Uttar Pradesh'],
        'Goa': ['Maharashtra', 'Karnataka'],
        'Gujarat': ['Maharashtra', 'Rajasthan', 'Dadra & Nagar Haveli', 'Daman & Diu', 'Madhya Pradesh'],
        'Haryana': ['Punjab', 'Himachal Pradesh', 'Delhi', 'Uttar Pradesh', 'Rajasthan', 'Chandigarh', 'Uttarakhand'],
        'Himachal Pradesh': ['Jammu & Kashmir', 'Punjab', 'Uttarakhand', 'Haryana', 'Chandigarh', 'Uttar Pradesh'],
        'Jammu & Kashmir': ['Himachal Pradesh', 'Punjab'],
        'Jharkhand': ['Bihar', 'Uttar Pradesh', 'Chhattisgarh', 'West Bengal', 'Odisha'],
        'Karnataka': ['Maharashtra', 'Goa', 'Andhra Pradesh', 'Tamil Nadu', 'Telangana', 'Kerala'],
        'Kerala': ['Karnataka', 'Tamil Nadu'],
        'Lakshadweep': [],
        'Madhya Pradesh': ['Rajasthan', 'Uttar Pradesh', 'Chhattisgarh', 'Gujarat', 'Maharashtra'],
        'Maharashtra': ['Gujarat', 'Madhya Pradesh', 'Chhattisgarh', 'Goa', 'Karnataka', 'Telangana', 'Daman & Diu', 'Dadra & Nagar Haveli'],
        'Manipur': ['Nagaland', 'Mizoram', 'Assam'],
        'Meghalaya': ['Assam'],
        'Mizoram': ['Assam', 'Manipur', 'Tripura'],
        'Nagaland': ['Arunachal Pradesh', 'Manipur', 'Assam'],
        'Odisha': ['West Bengal', 'Jharkhand', 'Chhattisgarh', 'Andhra Pradesh'],
        "Puducherry": ["Tamil Nadu"],
        "Punjab": ["Haryana", "Himachal Pradesh", "Jammu & Kashmir", 'Chandigarh', 'Rajasthan'],
        "Rajasthan": ["Punjab", "Haryana", "Uttar Pradesh", "Gujarat", "Madhya Pradesh", "Haryana"],
        "Sikkim": ["West Bengal"],
        "Tamil Nadu": ["Kerala", "Karnataka", "Andhra Pradesh", "Puducherry"],
        "Telangana": ["Maharashtra", "Andhra Pradesh", "Karnataka", "Chhattisgarh"],
        "Tripura": ["Assam", "Mizoram"],
        "Uttar Pradesh": ["Uttarakhand", "Himachal Pradesh", "Haryana", "Delhi", "Rajasthan", "Bihar", "Jharkhand", "Madhya Pradesh", "Chhattisgarh"],
        "Uttarakhand": ["Himachal Pradesh", "Uttar Pradesh", "Haryana"],
        "West Bengal": ["Sikkim", "Assam", "Jharkhand", "Odisha", "Bihar"],
    }

    return neighbors.get(state_name, [])
def find_nearby_pincodes(request, pincode=None):
    """
    API view to get nearby pincodes and distances based on the input pincode.
    """
    if pincode is None:
        return JsonResponse({'error': 'Pincode is required.'}, status=400)

    if request.method == 'GET':
        try:
            # Get the base pincode (current user location)
            user_location = get_object_or_404(Pincode, pincode=pincode)
        except Http404:
            return JsonResponse({'error': 'No Pincode matches the given query.'}, status=404)

        state_name = user_location.state_name

        # Get all pincodes in the same state
        nearby_pincodes = Pincode.objects.filter(state_name=state_name)

        # Also include pincodes from neighboring states
        neighboring_states = get_neighboring_states(state_name)
        if neighboring_states:
            nearby_pincodes = nearby_pincodes | Pincode.objects.filter(state_name__in=neighboring_states)

        # List to store nearby pincodes and their distances
        nearby_list = []
        for pincode_obj in nearby_pincodes:
            # Calculate the distance between current pincode and each nearby pincode
            distance = haversine(user_location.latitude, user_location.longitude,
                                 pincode_obj.latitude, pincode_obj.longitude)

            # Only include pincodes within 10 km and exclude the base pincode
            if distance <= 10 and pincode_obj.pincode != pincode:
                nearby_list.append({
                    'pincode': pincode_obj.pincode,
                    'distance': round(distance, 2),
                })

        # Sort the list by distance
        nearby_list.sort(key=lambda x: x['distance'])

        # Return the entire list of nearby pincodes within the 10 km radius
        return JsonResponse(nearby_list, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
