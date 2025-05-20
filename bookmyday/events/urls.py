from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path('register/', UserRegistrationAPI.as_view(), name='register'),
    path('login/', UserLoginAPI.as_view(), name='login'),
    path('logout/', UserLogoutAPI.as_view(), name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('booking/', BookingEventAPI.as_view(), name='booking'),
    path('booking/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
    path('attend/', AttendAPI.as_view(), name='attend')
]