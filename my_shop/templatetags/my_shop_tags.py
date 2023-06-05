from django import template
from my_shop.models import *

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.prefetch_related('sex').all()


@register.simple_tag()
def get_sexes():
    return Sex.objects.all()


@register.simple_tag()
def urlparams(request):
    params = []
    for key, value in request.GET.items():
        if key == 'page':
            continue
        params.append(f'{key}={value}')
    return '?' + '&'.join(params)


@register.simple_tag()
def pattern_range(start, stop):
    print(range(start, stop))
    return range(start, stop)
