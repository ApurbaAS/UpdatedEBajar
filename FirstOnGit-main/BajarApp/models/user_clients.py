from django.db import models
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

class User_Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    contact_number = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.first_name+ " "+self.last_name
    
    def send_verification_email(self, request):
        email = self.email
        subject = 'Email Verification'
        verification_link = self.generate_verification_link(request)
        message = f'Click the following link to verify your email: {verification_link}'
        from_email = 'Apurba007100@gmail.com'
        to_email = email
        email = EmailMessage(subject, message, from_email, [to_email])
        email.send()
        
    def generate_verification_link(self, request):
        current_site = get_current_site(request)
        return f'http://{current_site.domain}/verify-email/?email={self.email}'
    
    @staticmethod
    def get_user_email(email):
        try:
            return User_Client.objects.get(email = email)
        except:
            return False