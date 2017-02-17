from django import template
from products.models import Product

register = template.Library()


@register.inclusion_tag("products/block-finished.html")
def finished_tile(product):
    """
    Return a representation of a single product for display on the website
    """
    if(isinstance(product, str)):
        product = FinishedDecoy.objects.get(slug=product)

    return {"product": product}

