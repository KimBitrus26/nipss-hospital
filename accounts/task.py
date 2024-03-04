from celery import shared_task
import os

from django.conf import settings
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags
from twilio.rest import Client


@shared_task    
def send_otp_sms_task(otp_code, country_code, phone_number):

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
    print("========sent otp successfully=======")
    return "sms sent"

@shared_task    
def send_patient_file_number_sms_task(file_number, country_code, phone_number):

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


@shared_task
def send_signup_email_task(email, password, instance):
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


@shared_task
def send_patient_file_number_email_task(email, file_number, last_name):
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

@shared_task
def send_doctor_appointment_email_task(
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


@shared_task
def send_patient_appointment_approve_email_task(
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

@shared_task
def send_patient_appointment_approve_sms_task(
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


@shared_task    
def send_patient_payment_link_sms_task(amount, payment_link, country_code, phone_number):

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

@shared_task
def send_patient_payment_link_email_task(
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
