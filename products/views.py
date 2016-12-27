from django.shortcuts import render
from .models import ProductCategory, ProductType


def listing(category_slug, type_slug):
    """
    Display a product listing based on category and subcategory
    """

    prod_category = get_object_or_404(ProductCategory, slug=category_slug)
    prod_type = get_object_or_404(ProductType, slug=type_slug)

    #TODO: Figure out how to properly chain filters
    #products = Product.objects.filter().filter()
    products = {}

    return render('products/page-listing.html', {'products': products})
