from django.conf.urls import url
from django.urls import reverse_lazy
from oscar.apps.dashboard.app import DashboardApplication
from . import views


class SettingsDashboardApplication(DashboardApplication):

    # Set permissions for any new admin views
    default_permissions = ['is_staff', ]
    login_url = reverse_lazy('login-nextless')


    def get_urls(self):
        """
        Add our custom, snazzy URLs to the app
        """
        urls = super().get_urls()
        urls.append(url(r'^$', include('cart.dashboard.settings.urls')))
        return urls


application = SettingsDashboardApplication()

