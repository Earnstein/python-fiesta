from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag(name='get_google_api_key')
def get_google_api():
    return settings.GOOGLE_API_KEY