from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'phone_number', 'is_patient', 'is_receptionist', 
                    'is_doctor', 'is_phamacist', "is_lab_technician")
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', "phone_number", "country_code", 
        'is_phone_verified', 'is_profile_completed', 'is_patient', 'is_receptionist', 
        'is_doctor', 'is_phamacist', "is_lab_technician")}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
    )   
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2', 'send_password', "country_code", "phone_number", 
                    'is_profile_completed', 'is_phone_verified', 'is_patient', 'is_receptionist', 
                    'is_doctor', 'is_phamacist', "is_lab_technician", ),
    }),
) 
    search_fields = ('email',)
    ordering = ("-created_at",)

admin.site.register(User, CustomUserAdmin)
admin.site.register(OTPCode)
