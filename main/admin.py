from django.contrib import admin

from .models import SliderContent

@admin.register(SliderContent)
class SliderContentAdmin(admin.ModelAdmin):
    list_display = ('content', 'link')
    search_fields = ('content',)