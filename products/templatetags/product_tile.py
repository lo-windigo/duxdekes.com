from django import template
from products.models import Product

register = template.Library()


@register.inclusion_tag("products/block-product.html")
def product_tile(product):
    """
    Return a representation of a single product for display on the website
    """
    if(isinstance(product_value, str)):
        product = Product.objects.get(slug=product)

    return {"product": product}

