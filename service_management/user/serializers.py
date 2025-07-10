from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    
    class Meta:
        model = CustomUser
        fields = ['id','username','email','password','contact','address']
        
    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            contact=validated_data['contact'],
            address=validated_data['address'],
            
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','contact','address']
                
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)
    
    

    
        
        
    
