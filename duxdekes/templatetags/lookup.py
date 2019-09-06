
from django.template import Library

register = Library()


@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]
