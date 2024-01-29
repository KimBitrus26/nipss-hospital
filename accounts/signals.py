from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, OTPCode
from .utils import Helper

@receiver(post_save, sender=User)
def send_user_notifiactions(sender, instance, created, **kwargs):
    
    if created:
        
        if instance.is_patient:
                       
            otp = OTPCode.objects.create(user=instance)
            Helper.send_otp_sms(otp.code, instance.country_code, 
                                instance.phone_number)
            

        if instance.is_receptionist:
            instance.is_phone_verified = True
            instance.save()
            email, password = instance.email, instance.send_password
            Helper.send_signup_email(email, password, instance)

        if instance.is_doctor:
            instance.is_phone_verified = True
            instance.save()
            email, password = instance.email, instance.send_password
            Helper.send_signup_email(email, password, instance)


        if instance.is_phamacist:
            instance.is_phone_verified = True
            instance.save()
            email, password = instance.email, instance.send_password
            Helper.send_signup_email(email, password, instance)

        if instance.is_lab_technician:
            instance.is_phone_verified = True
            instance.save()
            email, password = instance.email, instance.send_password
            Helper.send_signup_email(email, password, instance)
