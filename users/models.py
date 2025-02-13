from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(
        upload_to='user_images/', blank=True, null=True, verbose_name='Аватар'
    )

    class Meta:
        db_table = 'user'
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username