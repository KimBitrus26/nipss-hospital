import datetime
import os
import requests

from django.conf import settings
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags
from django.urls import reverse
from twilio.rest import Client

from core.models import Transaction

class Helper:

    @staticmethod
    def reference_generator(random_string=""):
        return "rr_" + datetime.datetime.now().strftime("%m%d%y%H%M%S") + random_string

    @staticmethod    
    def send_otp_sms(otp_code, country_code, phone_number):

        # using twilio
        account_sid = os.environ['TWILIO_SID']
        auth_token = os.environ['TWILIO_TOKEN']
        client = Client(account_sid, auth_token)
        sms_body = f"Hi, Your account has be created on NIPSS HMS platform. Use this code {otp_code} to verify your phone number."
        message = client.messages.create(
            body=sms_body,
            from_=os.environ['TWILIO_NUMBER'],
            to=f"+{country_code}{phone_number}"
        )
        if not message.sid:
            raise ValueError(message.error_message)
        return "sms sent"
    
    @staticmethod    
    def send_patient_file_number_sms(file_number, country_code, phone_number):

        # using twilio
        account_sid = os.environ['TWILIO_SID']
        auth_token = os.environ['TWILIO_TOKEN']
        client = Client(account_sid, auth_token)
        sms_body = f"Hi, Your file was successfully opened on NIPSS HMS platform. The following is your file number {file_number}"
        message = client.messages.create(
            body=sms_body,
            from_=os.environ['TWILIO_NUMBER'],
            to=f"+{country_code}{phone_number}"
        )
        if not message.sid:
            raise ValueError(message.error_message)
        return "sms sent"

    
    @staticmethod
    def send_signup_email(email, password, instance):
        subject = "Account created"
        ctx = {
            "subject": subject,
            "email": email,
            "password": password,

        }
        html = "send_pharmacist_signup_email.html" if instance.is_phamacist else \
         "send_receptionist_email.html" if instance.is_receptionist else \
         "send_doctor_signup_email.html" if instance.is_doctor else \
         "send_lab_signup_email.html" if instance.is_lab_technician else \
         "send_patient_signup_email.html"
        html_msg = loader.render_to_string(html, ctx)
        txt_msg = strip_tags(html_msg)
        try:
            send_mail(
                subject,
                txt_msg,
                settings.DEFAULT_FROM_EMAIL,
                [email, ],
                fail_silently=False,
                html_message=html_msg
            )
        except BadHeaderError:
            pass

    
    @staticmethod
    def send_patient_file_number_email(email, file_number, last_name):
        subject = "File Number Created"
        ctx = {
            "subject": subject,
            "last_name": last_name,
            "file_number": file_number,

        }
        html = "send_patient_file_number_email.html"
        html_msg = loader.render_to_string(html, ctx)
        txt_msg = strip_tags(html_msg)
        try:
            send_mail(
                subject,
                txt_msg,
                settings.DEFAULT_FROM_EMAIL,
                [email, ],
                fail_silently=False,
                html_message=html_msg
            )
        except BadHeaderError:
            pass

    @staticmethod
    def send_doctor_appointment_email(
            doctor_email, 
            appointment_date,
            description
            ):
        subject = "New Appointment"
        ctx = {
            "subject": subject,
            "appointment_date": appointment_date,
            "description": description,         
        }
        html = "send_doctor_book_appointment_email.html"
        html_msg = loader.render_to_string(html, ctx)
        txt_msg = strip_tags(html_msg)
        try:
            send_mail(
                subject,
                txt_msg,
                settings.DEFAULT_FROM_EMAIL,
                [doctor_email, ],
                fail_silently=False,
                html_message=html_msg
            )
        except BadHeaderError:
            pass


    @staticmethod
    def send_patient_appointment_approve_email(
            email, 
            appoint_date
            ):
        subject = "Appointment Approved"
        ctx = {
            "subject": subject,
            "appoint_date": appoint_date,       
        }
        html = "send_patient_appointment_approved_email.html"
        html_msg = loader.render_to_string(html, ctx)
        txt_msg = strip_tags(html_msg)
        try:
            send_mail(
                subject,
                txt_msg,
                settings.DEFAULT_FROM_EMAIL,
                [email, ],
                fail_silently=False,
                html_message=html_msg
            )
        except BadHeaderError:
            pass
    
    @staticmethod
    def send_patient_appointment_approve_sms(
            country_code, 
            phone_number,
            appoint_date
            ):
        # using twilio
        account_sid = os.environ['TWILIO_SID']
        auth_token = os.environ['TWILIO_TOKEN']
        client = Client(account_sid, auth_token)
        sms_body = f"Hi, Your Doctor's appointment on NIPSS HMS platform has been approved for this date {appoint_date}"
        message = client.messages.create(
            body=sms_body,
            from_=os.environ['TWILIO_NUMBER'],
            to=f"+{country_code}{phone_number}"
        )
        if not message.sid:
            raise ValueError(message.error_message)
        return "sms sent"
    

    @staticmethod    
    def send_patient_payment_link_sms(amount, payment_link, country_code, phone_number):

        # using twilio
        account_sid = os.environ['TWILIO_SID']
        auth_token = os.environ['TWILIO_TOKEN']
        client = Client(account_sid, auth_token)
        sms_body = f"Hi, Your drugs have been valued for N{amount} on NIPSS HMS platform. Please click on the link below to make payment {payment_link}."
        message = client.messages.create(
            body=sms_body,
            from_=os.environ['TWILIO_NUMBER'],
            to=f"+{country_code}{phone_number}"
        )
        if not message.sid:
            raise ValueError(message.error_message)
        return "sms sent"
    
    @staticmethod
    def send_patient_payment_link_email(
            email, amount, payment_link
            ):
        subject = "Payment Link"
        ctx = {
            "subject": subject,
            "amount": amount, 
            "payment_link": payment_link,       
        }
        html = "send_patient_payment_link_email.html"
        html_msg = loader.render_to_string(html, ctx)
        txt_msg = strip_tags(html_msg)
        try:
            send_mail(
                subject,
                txt_msg,
                settings.DEFAULT_FROM_EMAIL,
                [email, ],
                fail_silently=False,
                html_message=html_msg
            )
        except BadHeaderError:
            pass
    

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
        