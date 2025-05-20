from rest_framework.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import *

# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser(
#             username= validated_data['username'],
#             email= validated_data['email'],
#             mobile_number= validated_data['mobile_number']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
class UserRegistrationSerializer(ModelSerializer):
    password1 = CharField(write_only=True)
    password2 = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email',    # 'first_name', 'last_name',
            'mobile_number', 'password1', 'password2'
        ]
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            password=validated_data['password1']
        )
        return user

class UserLoginSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise ValidationError("Invalid credentials")
        return user
    

class EventBookingSerializer(ModelSerializer):

    class Meta:
        model = EventBooking
        fields = [
            'title', 'description', 'on_date', 'location', 'owner'
        ]
        extra_kwargs = {
            'owner': {'read_only': True}
        }

    def validate(self, data):
        if EventBooking.objects.filter(on_date=data['on_date']).exists():
            raise ValidationError("This date is reserved already")
        return data

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return EventBooking.objects.create(**validated_data)
        # event = CustomUser.objects.create_user(
        #     title=validated_data['title'],
        #     description=validated_data['description'],
        #     on_date=validated_data['on_date'],
        #     location=validated_data['location'],

        # )
        # return event
    
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.on_date = validated_data.get('on_date', instance.on_date)
    #     instance.location = validated_data.get('location', instance.location)
    #     instance.save()
    #     return instance


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class EventAttendanceSerailzer(ModelSerializer):
    # event = PrimaryKeyRelatedField(querset=EventBooking.objects.all())
    class Meta:
        model = EventAttendance
        fields = ['event', 'attendee', 'attended_at']
        read_only_fields = ['attendee', 'attended_at']
        # extra_kwargs = {
        #     'attendee': {'read_only': True}
        # }

    def validate(self, attrs):
        request = self.context.get('request')
        event = attrs['event']

        if EventAttendance.objects.filter(event=event, attendee=request.user).exists():
            raise ValidationError("Entrance expired for this event!")
        return attrs