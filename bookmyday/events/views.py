# from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import *

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
from .serializers import *
from . import models
# from .permissons import IsOwnerOrReadOnly

# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate
# from django.contrib import messages
# from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout




# # Register user 
# @api_view(['POST'])
# def register_user(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# # Login User
# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         password = request.data.get('password')

#         user = None
#         if '@' in username:
#             try:
#                 user = CustomUser.objects.get(email=username)
#             except ObjectDoesNotExist:
#                 pass

#         if not user:
#             user = authenticate(username=username, password=password)

#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)

#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# 2
# @api_view(['POST'])
# def user_registration(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         mobile_number = request.POST.get('mobile_number')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if not all([username, email, mobile_number, password1, password2]):
#             return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if password1 == password2:
#             if CustomUser.objects.filter(username= username).exists():
#                 messages.info(request, 'Username not available.')
#                 raise ValueError("Username already Exists")

#             if CustomUser.objects.filter(email= email).exists():
#                 messages.info(request, 'Email not available.')
#                 raise ValueError("Eemail already Exists")
            
#             if CustomUser.objects.filter(mobile_number= mobile_number).exists():
#                 messages.info(request, 'Mobile number not available.')
#                 raise ValueError("Mobile number already Exists")
            
#             try:
#                 user = CustomUser.objects.create_user(
#                     username= username,
#                     first_name= first_name,
#                     last_name= last_name,
#                     email= email,
#                     mobile_number= mobile_number,
#                     password= password1
#                 )
#                 user.save()
#                 return Response({'Registerd User': user.username}, status=status.HTTP_200_OK)

#             except Exception as e:
#                 return Response({'error': str(e)}, status= status.HTTP_400_BAD_REQUEST)
                                                      
# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username= user_name, password= password)
#         if user is not None:
#             auth_login(request, user)
#             return Response({'Login': 'Success'}, status= status.HTTP_200_OK)
    
#         else:
#             messages.info(request, 'Invalid credentials')
#             return Response({'Login': 'Failed'}, status=status.HTTP_401_UNAUTHORIZED)
        

# @api_view(['POST'])
# def logout(request):
#     auth_logout(request)
#     return Response({'Logout': 'Success'}, status= status.HTTP_200_OK)

class UserRegistrationAPI(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': serializer.data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

class UserLoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        auth_login(request, user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'message': 'Login successful'
        })

class UserLogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        auth_logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    

class BookingEventAPI(CreateAPIView):
    serializer_class = EventBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     event = serializer.save()
    #     return Response({
    #         'event': serializer.data,
    #         'message': 'Event registered successfully'
    #     }, status=status.HTTP_201_CREATED)
    def get_serializer_context(self):
        # Pass the request object to the serializer context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

class BookingDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = EventBookingSerializer
    # permission_classes = [IsOwnerOrReadOnly]
    queryset = models.EventBooking.objects.all()

    # def perform_update(self, serializer):
    #     serializer.save()
    #     return serializer.data
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class AttendAPI(CreateAPIView):
    serializer_class = EventAttendanceSerailzer
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = EventAttendance.objects.all()

    def perform_create(self, serializer):
        serializer.save(attendee=self.request.user)
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     try:
    #         self.perform_create(serializer)
    #         return Response(
    #             {
    #                 'status': 'success',
    #                 'data': serializer.data,
    #                 'message': 'Welcome.'
    #             }
    #         )
        
    #     except Exception as e:
    #         return Response({
    #         'error': str(e)
    #     }, status=status.HTTP_400_BAD_REQUEST)
    
