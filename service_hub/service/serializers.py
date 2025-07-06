from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile , Category , Services

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()  
    address = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(
            user=user,
            contact=validated_data['contact'],
            address=validated_data['address']
        )

        return {
            "username": user.username,
            "email": user.email,
            "password": user.password, 
            "contact": validated_data['contact'],
            "address": validated_data['address']
        }
    
class UserProfileSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(source='profile.contact', required=False)
    address = serializers.CharField(source='profile.address', required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'contact', 'address']
        read_only_fields = ['id']

    def update(self, user, validated_data):
        profile_data = validated_data.pop('profile', {})

        user.username = validated_data.get('username', user.username)
        user.email = validated_data.get('email', user.email)
        user.save()

        profile = user.profile
        if 'contact' in profile_data:
            profile.contact = profile_data['contact']
        if 'address' in profile_data:
            profile.address = profile_data['address']
        profile.save()

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True, write_only=True)

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'