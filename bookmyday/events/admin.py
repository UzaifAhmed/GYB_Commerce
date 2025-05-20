from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EventBooking, EventAttendance

# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser

admin.site.register(CustomUser)
admin.site.register(EventBooking)
admin.site.register(EventAttendance)