from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pincode_app.urls')),  # This line includes the app's URLs
]
