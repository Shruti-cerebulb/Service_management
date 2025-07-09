from rest_framework import serializers
from .models import Category,Services,Employee,Booking
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class ServicesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')

    class Meta:
        model = Services
        fields = ['id', 'category', 'name', 'description', 'price', 'duration', 'created_at', 'updated_at']
        
class EmployeeRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    contact = serializers.CharField(source='user.contact')
    address = serializers.CharField(source='user.address')
    password = serializers.CharField(source='user.password', write_only=True, required=True, validators=[validate_password])

    services = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Services.objects.all(), required=False
    )

    class Meta:
        model = Employee
        fields = [
            'username', 'password', 'email', 'contact', 'address',
            'services', 'joining_date', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['joining_date', 'is_active', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        services = validated_data.pop('services', None)

        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        employee = Employee.objects.create(user=user, **validated_data)
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
        
class EmployeeLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    service_name = serializers.ReadOnlyField(source = 'service.name')
    employee_name = serializers.ReadOnlyField(source = 'employee.user.username')
    
    class Meta:
        model = Booking
        fields = ['id','user','service','service_name','employee','employee_name','appointment_date','status','notes','created_at','updated_at']
        read_only_fields = ['id','user','created_at','updated_at']
    
    
