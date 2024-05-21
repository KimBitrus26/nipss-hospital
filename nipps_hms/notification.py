import re
import requests
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from accounts.models import User

class Notifications:

    @staticmethod
    def send_push_notification(title, content, user):
            
        try:
            user_instance = User.objects.get(id=user.id)
        except Exception as e:
            print("Multiple user error : ", e)
            return
        
        if not user_instance.fcm_device_registered:
            print("User device not registered")
            return

        try:
            device = FCMDevice.objects.get(user=user_instance)
        except Exception as e:
            print("FCM FCMDevice not found : ", e)
            return
        
        print("device----", device)
       
        if not device.active:
            device.active = True
            device.save()
        
        try:
            response = device.send_message(Message(notification=Notification(title=title, body=content)))
        except Exception as e:
            print("FCM send message error:", e)
            
            return
        
        print("FCM response : ", response)
        return response


class NotificationMessages:

    @staticmethod
    def send_pharmarcist_prescription_notification():
        return f"Hi, New prescription for billing" 
               
    @staticmethod
    def send_lab_test_notification():
        return f"Hi, You have a new test to attend to" 
    
    @staticmethod
    def send_doctor_appointment_notification():
        return f"Hi Sir, You have a new patient appointment" 
    
    @staticmethod
    def send_doctor_appointment_completed_notification():
        return f"Hi Sir, patient appointment confirmed completed" 
               