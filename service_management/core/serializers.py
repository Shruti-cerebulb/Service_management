from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile,ServiceCategory,Service

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')
        
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    contact = serializers.CharField()
    address = serializers.CharField()

    def create(self, validated_data):
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create profile with contact and address
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
    
class ProfileSerializer(serializers.ModelSerializer):
    # Include Profile fields
    contact = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'contact', 'address']
        read_only_fields = ['id']  # id cannot be updated

    def update(self, instance, validated_data):

        # Update User fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update Profile fields
        profile = instance.profile
        profile.contact = validated_data.get('contact', profile.contact)
        profile.address = validated_data.get('address', profile.address)
        profile.save()

        return instance
        
        
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
    