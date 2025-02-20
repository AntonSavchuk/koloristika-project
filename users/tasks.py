from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_verification_email(subject, message, recipient_list):
    send_mail(subject, message, "noreply@koloristika.com", recipient_list)