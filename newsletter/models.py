from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Newsletter(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Контент (HTML)")
    font_size = models.IntegerField(default=16, verbose_name="Размер шрифта")
    text_color = models.CharField(max_length=7, default="#000000", verbose_name="Цвет текста") 
    background_image = models.ImageField(upload_to="newsletter_backgrounds/", blank=True, null=True, verbose_name="Фоновое изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title
