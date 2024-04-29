import six
from django.db import models
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
class UserType(models.TextChoices):
    USER = "USER", "User"
    AUTHOR = "AUTHOR", "Author"
    PUBLISHER = "PUBLISHER", "Publisher"
    ADMIN = "ADMIN", "Admin"
    SUPERUSER = "SUPERUSER", "Superuser"
    
    
    
class TokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.id)+six.text_type(timestamp)+six.text_type(user.is_email_confirmed))
    



def send_activation_email(data):
    
    email_subject = "Activate your account"
    email_body = render_to_string('odlauth/partials/template_activate_account.html', {
        'username' : data['username'],
        'domain' : data['domain'],
        'token': data['token']
    })
    
    email = EmailMessage(subject=email_subject, body=email_body, to=[data['email']])
    
    email.send()