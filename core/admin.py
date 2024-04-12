from django.contrib import admin
from .models import *

admin.site.register(PatientPrincipal)
admin.site.register(Doctor)
admin.site.register(AccountsRecords)
admin.site.register(Pharmacist)
admin.site.register(LabTechnician)
admin.site.register(Nurse)
admin.site.register(LabTestResult)
admin.site.register(Prescription)
admin.site.register(BookAppointment)
admin.site.register(Transaction)
admin.site.register(Spouse)
admin.site.register(Children)


admin.site.register(PrincipalContinuationSheet)
admin.site.register(SpouseContinuationSheet)
admin.site.register(ChildContinuationSheet)


admin.site.register(ChildPrescriptionForm)
admin.site.register(SpousePrescriptionForm)
admin.site.register(PrincipalPatientPrescriptionForm)

admin.site.register(ChildTestRequestSheet)
admin.site.register(SpouseTestRequestSheet)
admin.site.register(PrincipalPatientTestRequestSheet)
