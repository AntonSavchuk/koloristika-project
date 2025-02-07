from django import template
from services.models import Categories

register = template.Library()

@register.filter(name='highlight_koloristika')
def highlight_koloristika(text):
    return text.replace("Koloristika", '<span style="color: #43ab92; text-transform: uppercase;">Koloristika</span>')
