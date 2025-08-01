from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']

    # Fields to display on the user detail page in admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )

    # Fields to show on the user creation page in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    # Set email as username field for admin forms
    add_form_template = 'admin/auth/user/add_form.html'

admin.site.register(User, UserAdmin)
