"""duxdekes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
#from django.contrib import admin
from django.contrib.auth import views as auth_views
from oscar.app import application
from oscar.core.loading import get_class
from . import views
#admin.autodiscover()

listing = get_class('catalogue.views', 'CatalogueView')

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contact/?$', views.Contact.as_view(), name='contact'),
    #url(r'^products/', include('products.urls')),
    #url(r'^admin/', admin.site.urls),
    url(r'^listing/', listing.as_view()),
    url(r'', include(application.urls)),
    url(r'^login/$', auth_views.login, {
        'redirect_field_name': '',
    }, name='login-nextless'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

