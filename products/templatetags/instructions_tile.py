from django import template
from products.models import Product

register = template.Library()


@register.inclusion_tag("products/block-instructions.html")
def instructions_tile(product):
    """
    Return a representation of a single product for display on the website
    """
    if(isinstance(product, str)):
        product = Instructions.objects.get(slug=product)

    return {"product": product}

