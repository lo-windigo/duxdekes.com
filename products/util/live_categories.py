from .models import ProductCategory


def live_categories():
    """
    Returns a list of products, organized by category type, for any product
    categories that contain products
    """

    #TODO: This is fake syntax, please replace with actual filter when not
    # flying
    return ProductCategory.objects.filter(products.__COUNT__ > 0)

