from django.conf.urls import url
from oscar.core.loading import get_class
from oscar.apps.dashboard.app import DashboardApplication
from . import views


class DuxDashboardApplication(DashboardApplication):

    def get_urls(self):
        original_urls = super(DuxDashboardApplication, self).get_urls()
        custom_urls = [
            url(r'^unfinished/$',
                views.UnfinishedListView.as_view(),
                name='catalogue-unfinished'),
        ]

        urls = original_urls + custom_urls
        return self.post_process_urls(urls)


application = DuxDashboardApplication()

