from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'contact', 'address', 'is_staff')
    search_fields = ('username', 'email', 'contact')
 
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('contact', 'address')}),
    )
 
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('contact', 'address')}),
    )
