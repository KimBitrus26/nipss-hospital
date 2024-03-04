import datetime
import requests

from django.conf import settings
from django.urls import reverse

from core.models import Transaction
from .task import (send_doctor_appointment_email_task,
                   send_otp_sms_task,
                   send_patient_appointment_approve_email_task,
                   send_patient_appointment_approve_sms_task,
                   send_patient_file_number_email_task,
                   send_patient_file_number_sms_task,
                   send_patient_payment_link_email_task,
                   send_patient_payment_link_sms_task,
                   send_signup_email_task,
                   )

class Helper:

    @staticmethod
    def reference_generator(random_string=""):
        return "rr_" + datetime.datetime.now().strftime("%m%d%y%H%M%S") + random_string

    @staticmethod    
    def send_otp_sms(otp_code, country_code, phone_number):

        send_otp_sms_task.delay(otp_code, country_code, phone_number)
    
    @staticmethod    
    def send_patient_file_number_sms(file_number, country_code, phone_number):

        send_patient_file_number_sms_task.delay(file_number, country_code, phone_number)

    @staticmethod
    def send_signup_email(email, password, instance):

        send_signup_email_task.delay(email, password, instance)
        
    @staticmethod
    def send_patient_file_number_email(email, file_number, last_name):

        send_patient_file_number_email_task.delay(email, file_number, last_name)
       
    @staticmethod
    def send_doctor_appointment_email(
            doctor_email, 
            appointment_date,
            description
            ):
        
        send_doctor_appointment_email_task.delay(
            doctor_email, 
            appointment_date,
            description
            )
        
    @staticmethod
    def send_patient_appointment_approve_email(
            email, 
            appoint_date
            ):
        
        send_patient_appointment_approve_email_task.delay(
            email, 
            appoint_date
            )
        
    @staticmethod
    def send_patient_appointment_approve_sms(
            country_code, 
            phone_number,
            appoint_date
            ):
        
        send_patient_appointment_approve_sms_task.delay(
            country_code, 
            phone_number,
            appoint_date
            )
        
    @staticmethod    
    def send_patient_payment_link_sms(amount, payment_link, country_code, phone_number):

        send_patient_payment_link_sms_task.delay(amount, payment_link, country_code, phone_number)
        
    @staticmethod
    def send_patient_payment_link_email(
            email, amount, payment_link
            ):
        
        send_patient_payment_link_email_task.delay(
            email, amount, payment_link
            )
        
class PayStackRequestHelper:

    AUTHORIZED_HEADER = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY
    }
    BASE_URL = "https://api.paystack.co/"
    INITIALIZE_TRANSACTION_URL = BASE_URL + "transaction/initialize/"
    VERIFY_TRANSACTION_URL = BASE_URL + "transaction/verify/"

    @staticmethod
    def send_payment(patient_user, request, reference, email, amount, first_name, last_name):
        tx_data = {
            "reference": reference,
            "email": email,
            "amount": amount,
            "callback_url": request.build_absolute_uri(reverse('verify_transaction', kwargs={'ref': reference})),
            "metadata": {
                "first_name": first_name,
                "last_name": last_name,
                     
            }
        }
        res = requests.post(PayStackRequestHelper.INITIALIZE_TRANSACTION_URL,
                            headers=PayStackRequestHelper.AUTHORIZED_HEADER, json=tx_data)
        res_data = res.json()

        if res_data['status']:
            Transaction.objects.create(user=patient_user, ref=reference, email=email, amount=amount, first_name=first_name, last_name=last_name)
            return res_data
        else:
            return None
        