from django import template
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def get_image(image):
    if image and image.url:
        return image.url
    else:
        return static('img/no_image.png')
