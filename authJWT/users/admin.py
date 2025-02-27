# from django.contrib import admin

# from .models import User

# admin.site.register(User)  

# Register your models here.

from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Admin Dashboard"
admin.site.index_title = "Welcome to Admin Panel"
admin.site.site_title = "Django Admin"

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Ensure this line is present
    path('api/', include('users.urls')),  # ✅ API routes
]