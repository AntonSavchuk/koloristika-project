from allauth.account.signals import email_confirmation_sent
from allauth.account.models import EmailAddress

from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from .tasks import send_verification_email

User = get_user_model()

@receiver(post_save, sender=User)
def link_subscription_to_user(sender, instance, created, **kwargs):
    """ Привязывает email к пользователю после регистрации, если он уже был в подписке """
    if created:
        email_record = EmailAddress.objects.filter(email=instance.email, user=None).first()
        if email_record:
            email_record.user = instance
            email_record.primary = True
            email_record.save()


@receiver(email_confirmation_sent)
def send_verification_email_task(request, confirmation, **kwargs):
    current_site = get_current_site(request)
    subject = "Подтвердите ваш email"
    message = f"Перейдите по ссылке, чтобы подтвердить email: {current_site}/accounts/confirm-email/{confirmation.key}/"
    
    send_verification_email.delay(subject, message, [confirmation.email_address.email])


