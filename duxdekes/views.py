from django.shortcuts import render
from products.util import live_categories


def about(request):
    """
    About Dux Dekes' wood carvings
    """
    return render(request, 'duxdekes/page-about.html')


def about_artist(request):
    """
    About Jeff Duxbury
    """
    return render(request, 'duxdekes/page-about-artist.html')


def home(request):
    """
    The homepage: list the major product types, along with the categories, and a
    selection of the newest products.
    """

    #TODO: Get latest products for each type of category

    #TODO: create template
    return render(request, 'duxdekes/page-home.html')

