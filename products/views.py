from django.shortcuts import render
from .models import ProductCategory, ProductType


def listing(category_slug, type_slug):
    """
    Display a product listing based on category and subcategory
    """

    prod_category = get_object_or_404(ProductCategory, slug=category_slug)

    #TODO: get the proper syntax for get_list_or_404
    products = Product.objects.filter(category=prod_category)

    return render('products/page-listing.html', {'products': products})
