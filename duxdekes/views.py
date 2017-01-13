from django.shortcuts import render
from products.util import live_categories


def home(request):
    """
    The homepage
    """

    #TODO: Get latest products for each type of category

    #TODO: create template
    return render(request, 'duxdekes/page-home.html')

