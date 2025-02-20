from allauth.account.signals import email_confirmation_sent
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from .tasks import send_verification_email

@receiver(email_confirmation_sent)
def send_verification_email_task(request, confirmation, **kwargs):
    current_site = get_current_site(request)
    subject = "Подтвердите ваш email"
    message = f"Перейдите по ссылке, чтобы подтвердить email: {current_site}/accounts/confirm-email/{confirmation.key}/"
    
    send_verification_email.delay(subject, message, [confirmation.email_address.email])
