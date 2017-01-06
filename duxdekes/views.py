from django.shortcuts import render
from products.util import live_categories


def home():
    """
    The homepage
    """

    categories = live_categories()

    #TODO: Get latest products for each type of category

    #TODO: create template
    return render('products/page-listing.html', {'products': products})

