from django import template
from django.template.defaultfilters import stringfilter
from re import findall

register = template.Library()


@register.filter
@stringfilter
def numero(value):
    x = findall("..", value)
    return ".".join(x)


register.tag('numero', numero)