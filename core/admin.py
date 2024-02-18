from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Pharmacist)
admin.site.register(LabTechnician)
admin.site.register(Nurse)
admin.site.register(LabTestResult)
admin.site.register(Prescription)
admin.site.register(BookAppointment)
admin.site.register(Transaction)