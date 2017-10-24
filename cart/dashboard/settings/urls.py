from django.conf.urls import url
from . import views

app_name='settings'
urlpatterns = [
    url(r'^$', views.SettingsView.as_view(), name='index'),
]

