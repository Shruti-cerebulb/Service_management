from rest_framework import serializers
from .models import Category , Services , Employee , Booking
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from service.models import CustomUser


User = get_user_model()

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    # User fields
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    contact = serializers.CharField(source='user.contact')
    address = serializers.CharField(source='user.address')
    password = serializers.CharField(
        write_only=True, source='user.password', validators=[validate_password]
    )

    # Employee fields
    services = serializers.PrimaryKeyRelatedField(
        queryset=Services.objects.all(), many=True, required=False
    )

    joining_date = serializers.DateField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'username', 'email', 'password', 'contact', 'address',
            'services', 'joining_date', 'is_active', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = CustomUser.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            contact=user_data['contact'],
            address=user_data['address'],
        )

        employee = Employee.objects.create(user=user)

        services = validated_data.get('services')
        if services:
            employee.services.set(services)

        return employee
    
class EmployeeProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    contact = serializers.CharField(source='user.contact')
    address = serializers.CharField(source='user.address')

    services = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Employee
        fields = [ 'id', 'username', 'email', 'contact', 'address', 'services', 'joining_date', 'is_active', 'created_at','updated_at' ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if 'contact' in user_data:
            instance.user.contact = user_data['contact']
        if 'address' in user_data:
            instance.user.address = user_data['address']
        instance.user.save()
        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    service_name = serializers.ReadOnlyField(source='service.name')
    employee_name = serializers.ReadOnlyField(source='employee.user.username')

    class Meta:
        model = Booking
        fields = ['id','user','service','service_name','employee','employee_name',
                  'scheduled_date','status','notes','created_at','updated_at' ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']