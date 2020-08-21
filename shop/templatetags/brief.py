from django import template
from django.utils.text import Truncator


register = template.Library()

@register.filter
def brief(product):
    if product.brief:
        return product.brief
    else:
        words = product.description.split()[:20]
        brief_description = words = ' '.join(words)
        if len(words) > 20:
            brief_description += "..."
        return brief_description
