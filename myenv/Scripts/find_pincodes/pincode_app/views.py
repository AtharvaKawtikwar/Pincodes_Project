import math
from django.shortcuts import render
from .models import NearbyPincode, Pincode
from django.http import Http404

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
    """Return a list of neighboring states and union territories based on the given state name."""
    neighbors = {
        'Andaman & Nicobar Islands': [],
        'Andhra Pradesh': ['Telangana', 'Tamil Nadu', 'Karnataka', 'Odisha','Chhattisgarh'],
        'Arunachal Pradesh': ['Assam', 'Nagaland'],
        'Assam': ['Arunachal Pradesh', 'Nagaland', 'Manipur', 'Mizoram', 'West Bengal','Meghalaya', 'Tripura'],
        'Bihar': ['Uttar Pradesh', 'Jharkhand', 'West Bengal'],
        'Chhattisgarh': ['Madhya Pradesh', 'Odisha', 'Jharkhand', 'Telangana', 'Maharashtra','Andhra Pradesh', 'Uttar Pradesh'],
        'Dadra & Nagar Haveli': ['Gujarat', 'Maharashtra'],
        'Daman & Diu': ['Gujarat', 'Maharashtra'],
        'Delhi': ['Haryana', 'Uttar Pradesh'],
        'Goa': ['Maharashtra', 'Karnataka'],
        'Gujarat': ['Maharashtra', 'Rajasthan', 'Dadra & Nagar Haveli', 'Daman & Diu', 'Madhya Pradesh'],
        'Haryana': ['Punjab', 'Himachal Pradesh', 'Delhi', 'Uttar Pradesh', 'Rajasthan', 'Chandigarh','Uttarakhand'],
        'Himachal Pradesh': ['Jammu & Kashmir', 'Punjab', 'Uttarakhand', 'Haryana', 'Chandigarh','Uttar Pradesh'],
        'Jammu & Kashmir': ['Himachal Pradesh', 'Punjab'],  
        'Jharkhand': ['Bihar', 'Uttar Pradesh', 'Chhattisgarh', 'West Bengal', 'Odisha'],
        'Karnataka': ['Maharashtra', 'Goa', 'Andhra Pradesh', 'Tamil Nadu', 'Telangana', 'Kerala'],
        'Kerala': ['Karnataka', 'Tamil Nadu'],
        'Lakshadweep': [], 
        'Madhya Pradesh': ['Rajasthan', 'Uttar Pradesh', 'Chhattisgarh', 'Gujarat', 'Maharashtra'],
        'Maharashtra': ['Gujarat', 'Madhya Pradesh', 'Chhattisgarh', 'Goa', 'Karnataka', 'Telangana','Daman & Diu', 'Dadra & Nagar Haveli'],
        'Manipur': ['Nagaland', 'Mizoram', 'Assam'],
        'Meghalaya': ['Assam'],
        'Mizoram': ['Assam', 'Manipur', 'Tripura'],
        'Nagaland': ['Arunachal Pradesh', 'Manipur', 'Assam'],
        'Odisha': ['West Bengal', 'Jharkhand', 'Chhattisgarh','Andhra Pradesh'],
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

def find_nearby_pincodes(request):
    """Find nearby pincodes based on user input."""
    if request.method == 'POST':
        user_pincode = request.POST.get('pincode')
        
        try:
            user_location = Pincode.objects.get(pincode=user_pincode)
        except Pincode.DoesNotExist:
            raise Http404(f'Pincode "{user_pincode}" not found.')

        state_name = user_location.state_name
        
        # Get pincodes from the same state
        nearby_pincodes = Pincode.objects.filter(state_name=state_name)

        # Get pincodes from neighboring states
        neighboring_states = get_neighboring_states(state_name)
        if neighboring_states:
            nearby_pincodes |= Pincode.objects.filter(state_name__in=neighboring_states)

        nearby_list = []
        
        for pincode in nearby_pincodes:
            distance = haversine(user_location.latitude, user_location.longitude,
                                 pincode.latitude,
                                 pincode.longitude)
            if distance <= 10 and pincode.pincode != user_pincode:
                nearby_list.append({
                    'pincode': pincode.pincode,
                    'distance': distance,
                })

                # Save to NearbyPincode model
                NearbyPincode.objects.update_or_create(
                    base_pincode=user_location,
                    defaults={
                        'nearby_pincode': {
                            'pincode': pincode.pincode,
                            'latitude': pincode.latitude,
                            'longitude': pincode.longitude
                        }
                    }
                )

        # Sort by distance and limit to 10 results.
        nearby_list.sort(key=lambda x: x['distance'])
        
        return render(request, 'pincode_app/nearby_pincodes.html', {
            'nearby_list': nearby_list[:10]
        })

    return render(request, 'pincode_app/input_pincode.html')
