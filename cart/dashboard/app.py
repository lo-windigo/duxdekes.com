from django.conf.urls import url
from django.views.generic.base import RedirectView
from oscar.core.loading import get_class
from oscar.apps.dashboard.app import DashboardApplication
from . import views


class DuxDashboardApplication(DashboardApplication):

    def get_urls(self):
        urls = super(DuxDashboardApplication, self).get_urls()
        custom_urls = [
            url(r'^finished/$',
                views.FinishedListView.as_view(),
                name='catalogue-finished'),
            url(r'^unfinished/$',
                views.UnfinishedListView.as_view(),
                name='catalogue-unfinished'),
            url(r'unfinished/create/$',
                views.UnfinishedCreateRedirectView.as_view(),
                name='catalogue-unfinished-create'),
            url(r'unfinished/create/(?P<product_class_slug>[\w-]+)/$',
                views.UnfinishedCreateUpdateView.as_view(),
                name='catalogue-unfinished-create'),
        ]

        urls.extend(custom_urls)
        return self.post_process_urls(urls)


application = DuxDashboardApplication()

