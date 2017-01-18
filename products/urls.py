from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<category_slug>.+)/?$', views.listing, name='listing'),
]

