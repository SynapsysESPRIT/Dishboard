from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client, Professional, Provider, Admin

# Custom User Admin
class UserAdmin(BaseUserAdmin):
    # Define the fields to display in the list view of the admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    # Customize the fieldsets to include additional fields for User model
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'age', 'gender', 'address', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # Removed 'date_joined'
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'is_staff', 'is_active')
        }),
    )

# Client Admin
class ClientAdmin(UserAdmin):
    # Customize the list display to include client-specific fields
    list_display = ('username', 'email', 'first_name', 'last_name', 'weight', 'height', 'bmi')
    fieldsets = UserAdmin.fieldsets + (
        ('Client Info', {'fields': ('weight', 'height', 'bmi')}),
    )

# Professional Admin
class ProfessionalAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'years_of_experience', 'diploma', 'cin', 'matricule')
    fieldsets = UserAdmin.fieldsets + (
        ('Professional Info', {'fields': ('years_of_experience', 'diploma', 'cin', 'matricule')}),
    )

# Provider Admin
class ProviderAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'company_name', 'tax_code')
    fieldsets = UserAdmin.fieldsets + (
        ('Provider Info', {'fields': ('company_name', 'tax_code')}),
    )

# Admin Admin
class AdminAdmin(UserAdmin):
    # Any custom fields specific to Admin role can be added here
    pass

# Register models with custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Professional, ProfessionalAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Admin, AdminAdmin)
