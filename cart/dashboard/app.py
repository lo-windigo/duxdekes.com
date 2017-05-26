from django.conf.urls import url
from django.views.generic.base import RedirectView
from oscar.core.loading import get_class
from oscar.apps.dashboard.app import DashboardApplication
from . import views


class DuxDashboardApplication(DashboardApplication):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^finished/$',
                views.FinishedListView.as_view(),
                name='catalogue-finished-list'),
            url(r'finished/(?P<pk>\d+)/$',
                views.FinishedUpdateView.as_view(),
                name='catalogue-finished'),
            url(r'finished/create/$',
                views.FinishedCreateView.as_view(),
                name='catalogue-finished-create'),
            url(r'finished/delete/(?P<pk>\d+)/$',
                views.FinishedDeleteView.as_view(),
                name='catalogue-finished-delete'),
            url(r'^unfinished/$',
                views.UnfinishedListView.as_view(),
                name='catalogue-unfinished-list'),
            url(r'unfinished/(?P<pk>\d+)/$',
                views.UnfinishedUpdateView.as_view(),
                name='catalogue-unfinished'),
            url(r'unfinished/create/$',
                views.UnfinishedCreateView.as_view(),
                name='catalogue-unfinished-create'),
            url(r'unfinished/delete/(?P<pk>\d+)/$',
                views.UnfinishedDeleteView.as_view(),
                name='catalogue-unfinished-delete'),
        ]

        urls.extend(custom_urls)
        return self.post_process_urls(urls)


application = DuxDashboardApplication()

