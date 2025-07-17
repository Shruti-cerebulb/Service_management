from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from django.core.mail import send_mail
import re
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
        class Meta:
             model = CustomUser
             fields =  ['id','username', 'email','contact','address'] 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    address = serializers.CharField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'contact', 'address']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_contact(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise serializers.ValidationError("Contact must be a 10-digit number.")
        return value
          
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  
            contact=validated_data['contact'],
            address=validated_data['address'],
        )

        subject = "Welcome to Service Hub"
        message = f"Hi {user.username},\n\nThank you for registering with ServiceHub. We're happy to have you!"
        from_email = None
        recipient_list = [user.email]

        send_mail(subject,message,from_email,recipient_list,fail_silently=False)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True, write_only=True)

    