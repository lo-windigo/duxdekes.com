from django.urls import reverse_lazy
from django.conf.urls import include, url
from oscar.apps.dashboard.app import (
    DashboardApplication as BaseDashboardApplication)
from .catalogue import views


class DashboardApplication(BaseDashboardApplication):
    name = 'dashboard'
    app_name = 'dashboard'
    default_permissions = ['is_staff', ]
    login_url = reverse_lazy('login-nextless')

    def get_urls(self):
        """
        Add our custom, snazzy URLs to the app
        """
        urls = super().get_urls()
        custom_urls = [
            url(r'^finished/$',
                views.FinishedListView.as_view(),
                name='catalogue-finished-list'),
            url(r'^finished/(?P<pk>\d+)/$',
                views.FinishedUpdateView.as_view(),
                name='catalogue-finished'),
            url(r'^finished/create/$',
                views.FinishedCreateView.as_view(),
                name='catalogue-finished-create'),
            url(r'^finished/delete/(?P<pk>\d+)/$',
                views.FinishedDeleteView.as_view(),
                name='catalogue-finished-delete'),
            url(r'^unfinished/$',
                views.UnfinishedListView.as_view(),
                name='catalogue-unfinished-list'),
            url(r'^unfinished/(?P<pk>\d+)/$',
                views.UnfinishedUpdateView.as_view(),
                name='catalogue-unfinished'),
            url(r'^unfinished/create/$',
                views.UnfinishedCreateView.as_view(),
                name='catalogue-unfinished-create'),
            url(r'^unfinished/delete/(?P<pk>\d+)/$',
                views.UnfinishedDeleteView.as_view(),
                name='catalogue-unfinished-delete'),
            url(r'^instructions/$',
                views.InstructionsListView.as_view(),
                name='catalogue-instructions-list'),
            url(r'^instructions/(?P<pk>\d+)/$',
                views.InstructionsUpdateView.as_view(),
                name='catalogue-instructions'),
            url(r'^instructions/create/$',
                views.InstructionsCreateView.as_view(),
                name='catalogue-instructions-create'),
            url(r'^instructions/delete/(?P<pk>\d+)/$',
                views.InstructionsDeleteView.as_view(),
                name='catalogue-instructions-delete'),
            url(r'^shipping/', include('cart.dashboard.shipping.urls')),
        ]

        urls.extend(custom_urls)
        return urls


application = DashboardApplication()

