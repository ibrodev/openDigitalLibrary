from celery import shared_task
from .utils import send_activation_email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


@shared_task
def send_activation_link(data):
    email_subject = "Activate your account"
    email_body = render_to_string('odlauth/partials/template_activate_account.html', {
        'username' : data['username'],
        'domain' : data['domain'],
        'token': data['token']
    })
    
    EmailMessage(subject=email_subject, body=email_body, to=[data['email']]).send()
    
    return None