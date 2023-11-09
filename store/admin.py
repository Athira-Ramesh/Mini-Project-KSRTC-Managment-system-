#from django.contrib import admin
#from . models import Staff
# Register your models here.
#admin.site.register(Staff)
#from django.contrib import admin
#from .models import CustomUser  # Import your model

#admin.site.register(CustomUser)  # Register your model with the admin interface


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

