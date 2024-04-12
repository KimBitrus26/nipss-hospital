from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import json

from django.utils.html import strip_tags

from .models import (Doctor, Pharmacist, LabTechnician, 
                     BookAppointment, PatientPrincipal, PrincipalContinuationSheet,
                      ChildContinuationSheet, Spouse, Children,
                      SpouseContinuationSheet, PrincipalPatientPrescriptionForm,
                      SpousePrescriptionForm, ChildPrescriptionForm,
                      PrincipalPatientTestRequestSheet, SpouseTestRequestSheet,
                      ChildTestRequestSheet,
                      
                      )

from nipps_hms.notification import Notifications, NotificationMessages
from accounts.models import User

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
        

@receiver(post_save, sender=PrincipalPatientPrescriptionForm)
def send_prescription_notification(sender, instance, created, **kwargs):
    
    if created:

        content = NotificationMessages.send_pharmarcist_prescription_notification()
        title = "NEW PRESCRIPTION" 
        url = f"http://localhost:5000/notify" 
    
        AUTHORIZED_HEADER = {
                "Content-Type": "application/json",
            }
        users = list(filter(lambda _user: _user.is_pharmacist == True, User.objects.all()))
        for user in users:
            print("user pharmacist", user)
            Notifications.send_push_notification(
                title, strip_tags(content), user

                )
            
            tx_data = {
                    "userId": user.slug,
                    "message": content + f" for Main patient ({instance.principal_patient.last_name}, {instance.principal_patient.first_name}) {instance.principal_patient.file_number}"
                    }
            response = requests.post(url=url, headers=AUTHORIZED_HEADER, data=json.dumps(tx_data))
            
            print("send res=======: ",response)
        

@receiver(post_save, sender=SpousePrescriptionForm)
def send_spouse_prescription_notification(sender, instance, created, **kwargs):
    
    if created:

        content = NotificationMessages.send_pharmarcist_prescription_notification()
        title = "NEW PRESCRIPTION" 
        url = f"http://localhost:5000/notify" 
    
        AUTHORIZED_HEADER = {
                "Content-Type": "application/json",
            }
        users = list(filter(lambda _user: _user.is_pharmacist == True, User.objects.all()))
        for user in users:
            print("user pharmacist", user)
            Notifications.send_push_notification(
                title, strip_tags(content), user
            )
            
            tx_data = {
                    "userId": user.slug,
                    "message": content + f" for Spouse patient ({instance.spouse.last_name}, {instance.spouse.first_name}) {instance.spouse.spouse_patient.file_number}"
                    }
            response = requests.post(url=url, headers=AUTHORIZED_HEADER, data=json.dumps(tx_data))
            
            print("send res=======: ",response)

@receiver(post_save, sender=ChildPrescriptionForm)
def send_child_prescription_notification(sender, instance, created, **kwargs):
    
    if created:

        content = NotificationMessages.send_pharmarcist_prescription_notification()
        title = "NEW PRESCRIPTION" 

        url = f"http://localhost:5000/notify" 
    
        AUTHORIZED_HEADER = {
                "Content-Type": "application/json",
            }
       
        users = list(filter(lambda _user: _user.is_pharmacist == True, User.objects.all()))
        for user in users:
            print("user pharmacist", user)
            Notifications.send_push_notification(
                title, strip_tags(content), user

            )     
            
            tx_data = {
                    "userId": user.slug,
                    "message": content + f" for Child patient ({instance.child.last_name}, {instance.child.first_name}) {instance.child.patient_principal.file_number}"
                    }
            response = requests.post(url=url, headers=AUTHORIZED_HEADER, data=json.dumps(tx_data))
            
            print("send res=======: ",response)  
        

@receiver(post_save, sender=PrincipalPatientTestRequestSheet)
def send_test_notification(sender, instance, created, **kwargs):
    
    if created:

        content = NotificationMessages.send_lab_test_notification()
        title = "NEW TEST" 
        url = "http://127.0.0.1:5000/notify" 
    
        AUTHORIZED_HEADER = {
                "Content-Type": "application/json",
            }
       
        users = list(filter(lambda _user: _user.is_lab_technician == True, User.objects.all()))
        for user in users:
            
            Notifications.send_push_notification(
                title, strip_tags(content), user

            )
           
            tx_data = {
                    "userId": user.slug,
                    "message": content + f" for Main patient ({instance.principal_patient.last_name}, {instance.principal_patient.first_name}) {instance.principal_patient.file_number}"
                    }
            response = requests.post(url=url, headers=AUTHORIZED_HEADER, data=json.dumps(tx_data))
            
            print("send res=======: ",response)

@receiver(post_save, sender=SpouseTestRequestSheet)
def send_spouse_test_notification(sender, instance, created, **kwargs):
    
    if created:

        content = NotificationMessages.send_lab_test_notification()
        title = "NEW TEST" 
        url = "http://127.0.0.1:5000/notify" 
    
        AUTHORIZED_HEADER = {
                "Content-Type": "application/json",
            }
       
        users = list(filter(lambda _user: _user.is_lab_technician == True, User.objects.all()))
        for user in users:
            
            Notifications.send_push_notification(
                title, strip_tags(content), user

            )

            tx_data = {
                    "userId": user.slug,
                    "message": content + f" for Spouse patient ({instance.spouse.last_name}, {instance.spouse.first_name}) {instance.spouse.spouse_patient.file_number}"
                    }
            response = requests.post(url=url, headers=AUTHORIZED_HEADER, data=json.dumps(tx_data))
            
            print("send res=======: ",response)

@receiver(post_save, sender=ChildTestRequestSheet)
def send_child_test_notification(sender, instance, created, **kwargs):
    
    if created:

        content = NotificationMessages.send_lab_test_notification()
        title = "NEW TEST" 
        url = "http://127.0.0.1:5000/notify" 
    
        AUTHORIZED_HEADER = {
                "Content-Type": "application/json",
            }
       
        users = list(filter(lambda _user: _user.is_lab_technician == True, User.objects.all()))
        for user in users:
            
            Notifications.send_push_notification(
                title, strip_tags(content), user

            )
            import json
            tx_data = {
                    "userId": user.slug,
                    "message": content + f" for Child patient ({instance.child.last_name}, {instance.child.first_name}) {instance.child.patient_principal.file_number}"
                    }
            response = requests.post(url=url, headers=AUTHORIZED_HEADER, data=json.dumps(tx_data))
            
            print("send res=======: ", response)


@receiver(post_save, sender=BookAppointment)
def send_doctor_appointment_notification(sender, instance, created, **kwargs):
    
    if created:

        content = NotificationMessages.send_doctor_appointment_notification()
        
        url = "http://127.0.0.1:5000/notify" 
    
        AUTHORIZED_HEADER = {
                "Content-Type": "application/json",
            }
       
        user = instance.doctor_user  
        
        import json
        tx_data = {
                "userId": user.slug,
                "message": content + f" for patient ({instance.patient.last_name}) {instance.patient.file_number}"
                }
        response = requests.post(url=url, headers=AUTHORIZED_HEADER, data=json.dumps(tx_data))
        
        print("send res=======: ", response)

    if instance.is_attended:

        content = NotificationMessages.send_doctor_appointment_completed_notification()
        
        url = "http://127.0.0.1:5000/notify" 
    
        AUTHORIZED_HEADER = {
                "Content-Type": "application/json",
            }
       
        user = instance.doctor_user  
        
        import json
        tx_data = {
                "userId": user.slug,
                "message": content + f" for patient ({instance.patient.last_name}) {instance.patient.file_number}"
                }
        response = requests.post(url=url, headers=AUTHORIZED_HEADER, data=json.dumps(tx_data))
        
        print("send res=======: ", response)
        
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