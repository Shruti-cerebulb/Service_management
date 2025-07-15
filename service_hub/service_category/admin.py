from django.contrib import admin
from .models import Category, Services, Employee, Booking
from import_export.admin import ImportExportModelAdmin
from .resources import CategoryResource, ServicesResource , EmployeeResource , BookingResource
import random
from django.core.exceptions import ValidationError
from django.contrib import messages


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ['id', 'name', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['created_at']
 
 
@admin.register(Services)
class ServicesAdmin(ImportExportModelAdmin):
    resource_class = ServicesResource
    list_display = ['id', 'name', 'category', 'price', 'duration', 'created_at', 'updated_at']
    search_fields = ['name', 'category__name']
    list_filter = ['category']
    ordering = ['created_at']


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ['id', 'user', 'joining_date', 'is_active','is_available', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['is_active', 'joining_date','is_available']
    ordering = ['-created_at']


@admin.register(Booking)
class BookingAdmin(ImportExportModelAdmin):
    resource_class = BookingResource
    list_display = ['id', 'user', 'service', 'employee', 'scheduled_date', 'status', 'created_at']
    search_fields = ['user__username', 'service__name', 'employee__user__username']
    list_filter = ['status', 'scheduled_date']
    ordering = ['-created_at']
    exclude = ('employee',)
 
    def save_model(self, request, obj, form, change):
        service = obj.service
        available_employees = service.employees.filter(is_active=True, is_available=True)
 
        if available_employees.exists():
            assigned_employee = random.choice(available_employees)
            obj.employee = assigned_employee
            messages.success(request, f"Employee '{assigned_employee}' was automatically assigned.")
        else:
            obj.employee = None  
            messages.warning(request, "No active employee available for this service right now. Please assign later.")
 
        super().save_model(request, obj, form, change)

