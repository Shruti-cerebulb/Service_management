from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget,ManyToManyWidget
from .models import Category, Services, Employee, Booking,User

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at', 'updated_at')
        export_order = ('id', 'name', 'created_at', 'updated_at')

class ServicesResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )

    class Meta:
        model = Services
        fields = ('id', 'name', 'category', 'price', 'duration', 'created_at', 'updated_at')
        export_order = ('id', 'name', 'category', 'price', 'duration', 'created_at', 'updated_at')
        
class EmployeeResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username') 
    )
    services = fields.Field(
        column_name='services',
        attribute='services',
        widget=ManyToManyWidget(Services, field='name', separator=',')
    )

    class Meta:
        model = Employee
        fields = ('id', 'user', 'services', 'joining_date', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'user', 'services', 'joining_date', 'is_active', 'created_at', 'updated_at')
        
class BookingResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username') 
    )
    service = fields.Field(
        column_name='service',
        attribute='service',
        widget=ForeignKeyWidget(Services, 'name') 
    )
    employee = fields.Field(
        column_name='employee',
        attribute='employee',
        widget=ForeignKeyWidget(Employee, 'user__username')  
    )

    class Meta:
        model = Booking
        fields = ('id', 'user', 'service', 'employee', 'appointment_date', 'status', 'notes', 'created_at', 'updated_at')
        export_order = ('id', 'user', 'service', 'employee', 'appointment_date', 'status', 'notes', 'created_at', 'updated_at')