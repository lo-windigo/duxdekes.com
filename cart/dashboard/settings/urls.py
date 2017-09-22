from django.conf.urls import url
from . import views

app_name='settings'
urlpatterns = [
    url(r'^$', views.SquareSettingsView.as_view(), name='index'),
]

