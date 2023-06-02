from django import template
from my_shop.models import *

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.prefetch_related('sex').all()


@register.simple_tag()
def get_sexes():
    return Sex.objects.all()
