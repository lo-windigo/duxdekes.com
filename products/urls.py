from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<cat>.+)/(?P<type>.+)/?$', views.listing, name='listing'),
]
