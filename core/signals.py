from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (Doctor, Pharmacist, LabTechnician, 
                     BookAppointment, PatientPrincipal, PrincipalContinuationSheet,
                      ChildContinuationSheet, Spouse, Children,
                      SpouseContinuationSheet,)
# from accounts.models import APPROVED
# from accounts.utils import Helper



@receiver(post_save, sender=PatientPrincipal)
def create_principal_continuation_sheet(sender, instance, created, **kwargs):
    
    if created and not PrincipalContinuationSheet.objects.filter(patient_principal=instance).exists():
        
        PrincipalContinuationSheet.objects.create(patient_principal=instance)

@receiver(post_save, sender=Spouse)
def create_principal_continuation_sheet(sender, instance, created, **kwargs):
    
    if created and not SpouseContinuationSheet.objects.filter(spouse=instance).exists():
        
        SpouseContinuationSheet.objects.create(spouse=instance)

@receiver(post_save, sender=Children)
def create_principal_continuation_sheet(sender, instance, created, **kwargs):
    
    if created and not ChildContinuationSheet.objects.filter(child=instance).exists():
        
        ChildContinuationSheet.objects.create(child=instance)
        
        

# @receiver(post_save, sender=Doctor)
# def send_user_notifiactions(sender, instance, created, **kwargs):
    
#     if created:
        
#         instance.user.is_profile_completed = True
#         instance.user.save()

# @receiver(post_save, sender=Patient)
# def send_user_notifiactions(sender, instance, created, **kwargs):
    
#     if created:
        
#         instance.user.is_profile_completed = True
#         instance.user.save()

# @receiver(post_save, sender=AdminReceptionist)
# def send_user_notifiactions(sender, instance, created, **kwargs):
    
#     if created:
        
#         instance.user.is_profile_completed = True
#         instance.user.save()

# @receiver(post_save, sender=LabTechnician)
# def send_user_notifiactions(sender, instance, created, **kwargs):
    
#     if created:
        
#         instance.user.is_profile_completed = True
#         instance.user.save()

# @receiver(post_save, sender=Pharmacist)
# def send_user_notifiactions(sender, instance, created, **kwargs):
    
#     if created:
        
#         instance.user.is_profile_completed = True
#         instance.user.save()

# @receiver(post_save, sender=BookAppointment)
# def send_book_appointment_notifiactions(sender, instance, created, **kwargs):
    
#     if created:
#         doctor_email = instance.doctor.email
#         appointment_date = instance.appointment_date
#         description = instance.description

        
#         Helper.send_doctor_appointment_email(
#             doctor_email, 
#             appointment_date,
#             description
#             )
        
#     if instance.status == APPROVED:
#         email = instance.patient.email
#         appoint_date = instance.appointment_date
#         country_code = instance.patient.country_code
#         phone_number = instance.patient.phone_number

#         Helper.send_patient_appointment_approve_email(
#             email, 
#             appoint_date
#             )
#         Helper.send_patient_appointment_approve_sms(
#             country_code, 
#             phone_number,
#             appoint_date
#             )