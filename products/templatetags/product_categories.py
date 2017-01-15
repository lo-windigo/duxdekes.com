from django import template
from products.models import ProductCategory

register = template.Library()


@register.inclusion_tag("products/block-navigation.html")
def product_categories():
    """
    Return a set of nested lists that represent the product categories, sorted
    by major type
    """

    categories = ProductCategory.objects.exclude(hidden=True)
    return {"categories": categories}

