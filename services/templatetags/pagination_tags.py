from django import template
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def preserve_query_params(context, **kwargs):
    """
    Сохраняет текущие GET-параметры и добавляет/изменяет переданные.
    """
    request = context['request']
    query_params = request.GET.copy() 

    for key, value in kwargs.items():
        query_params[key] = value

    encoded_query = query_params.urlencode()

    return f"?{encoded_query}" if encoded_query else "?"
