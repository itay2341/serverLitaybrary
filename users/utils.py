import random
from django.core.mail import EmailMessage
from .models import NewUser

class Util:
    @staticmethod
    def send_email(data):
        otp = random.randint(1000,9999)
        massage = f"Your OTP is {otp}"
        email = EmailMessage(subject=data['subject'],body=massage,to=[data['email']])
        email.send()
        user = NewUser.objects.get(email=data['email'])
        user.otp = otp
        user.save()