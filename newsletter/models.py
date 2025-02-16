from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

class Newsletter(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextUploadingField(verbose_name='Контент (HTML)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title
