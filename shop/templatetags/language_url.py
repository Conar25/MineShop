import os

from django import template


register = template.Library()


@register.filter
def language_url(path, language_code):
    return '/' + language_code + path[3:]
