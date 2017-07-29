from django.conf.urls import url
from . import views

app_name='shipping'
urlpatterns = [
    url(r'^$',
        views.BoxListView.as_view(),
        name='box-list'),
    url(r'^create/$',
        views.BoxCreateView.as_view(),
        name='box-create'),
    url(r'^(?P<pk>\d+)$',
        views.BoxUpdateView.as_view(),
        name='box-update'),
    url(r'^delete/(?P<pk>\d+)$',
        views.BoxDeleteView.as_view(),
        name='box-delete'),
]

