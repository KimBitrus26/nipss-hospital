from django.contrib import admin
from .models import *

admin.site.register(PatientPrincipal)
admin.site.register(Doctor)
admin.site.register(Pharmacist)
admin.site.register(LabTechnician)
admin.site.register(Nurse)
admin.site.register(LabTestResult)
admin.site.register(Prescription)
admin.site.register(BookAppointment)
admin.site.register(Transaction)
admin.site.register(Spouse)
admin.site.register(Children)