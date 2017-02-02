from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product


def listing(request, category_slug):
    """
    Display a product listing based on category and subcategory
    """

    prod_category = get_object_or_404(ProductCategory,
            slug=category_slug,
            hidden=False)
    products = Product.objects.exclude(hidden=True).filter(category=prod_category)
    context = {
            'products': products,
            'category': prod_category,
            }

    return render(request, 'products/page-listing.html', context)

