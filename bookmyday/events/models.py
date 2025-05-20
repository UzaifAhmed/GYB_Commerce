from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as g_l

# Create your models here.
class CustomUserManager(BaseUserManager):
    use_in_migrations=True

    def _create_user(self, username, email, mobile_number, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not mobile_number:
            raise ValueError('Mobile number is required')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, mobile_number=mobile_number, password=None, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, mobile_number, password, **extra_fields)

    def create_superuser(self, username, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, email, mobile_number, password, **extra_fields)
    
    # 
    # email = models.EmailField(unique=True)
    
class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True, error_messages={
        'unique': g_l("User with this mobile number already exists.")
    })

    REQUIRED_FIELDS = ['email', 'mobile_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class EventBooking(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    on_date = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    location = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')

    def __str__(self):
        return self.title

class EventAttendance(models.Model):
    event = models.ForeignKey(EventBooking, on_delete=models.CASCADE)
    attendee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attended_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['event', 'attendee']
    #     ordering = ['-attended_at']