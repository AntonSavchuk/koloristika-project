from django.db import models

class SliderContent(models.Model):
    content = models.TextField(
        verbose_name='Описание контента'
    )
    slider_photo = models.ImageField(
        upload_to='slider-info/', verbose_name='Фото на слайдере'
    )
    link = models.URLField(
        blank=True, null=True, verbose_name='Ссылка на мероприятие'
    )

    class Meta:
        db_table = 'slider_content'
        verbose_name = 'слайдера'
        verbose_name_plural = 'слайдеры'
        ordering = ['id']

    def __str__(self):
        return 'Контент слайдера'