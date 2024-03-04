from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_nurse',  'is_account',
                    'is_doctor', 'is_pharmacist', "is_lab_technician")
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_profile_completed', 'is_nurse',   'is_account',
        'is_doctor', 'is_pharmacist', "is_lab_technician")}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
    )   
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2', 'send_password', 
                    'is_profile_completed', 'is_nurse',  'is_account', 
                    'is_doctor', 'is_pharmacist', "is_lab_technician", ),
    }),
) 
    search_fields = ('email',)
    ordering = ("-created_at",)

admin.site.register(User, CustomUserAdmin)
