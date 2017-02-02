from products.models import ProductCategory


def live_categories():
    """
    Returns a list of products, organized by category type, for any product
    categories that contain products
    """

    # TODO: Maybe a little more sophistication is called for.
    return ProductCategory.objects.exclude(hidden=True)

