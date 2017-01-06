from django.shortcuts import render
from .models import ProductCategory, ProductType


def listing(category_slug):
    """
    Display a product listing based on category and subcategory
    """

    prod_category = get_object_or_404(ProductCategory, slug=category_slug)
    products = Product.objects.filter(category=prod_category)

    #TODO: create template
    return render('products/page-listing.html', {'products': products})
