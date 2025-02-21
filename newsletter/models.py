from django.db import models
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()

class Newsletter(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Контент (HTML)")
    font_size = models.IntegerField(default=16, verbose_name="Размер шрифта")
    text_color = models.CharField(max_length=7, default="#000000", verbose_name="Цвет текста") 
    background_image = models.ImageField(upload_to="newsletter_backgrounds/", blank=True, null=True, verbose_name="Фоновое изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not EmailAddress.objects.filter(email=self.email).exists():
            EmailAddress.objects.create(email=self.email, verified=False, primary=False, user=None)


    def __str__(self):
        return self.mail