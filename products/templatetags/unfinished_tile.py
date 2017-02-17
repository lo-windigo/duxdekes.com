from django import template
from products.models import Product

register = template.Library()


@register.inclusion_tag("products/block-unfinished.html")
def unfinished_tile(product):
    """
    Return a representation of a single product for display on the website
    """
    if(isinstance(product, str)):
        product = UnfinishedDecoy.objects.get(slug=product)

    return {"product": product}

