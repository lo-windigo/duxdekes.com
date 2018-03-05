from django.conf.urls import url
from oscar.apps.dashboard.orders.app import OrdersDashboardApplication as OscarODApp
from . import views


class OrdersDashboardApplication(OscarODApp):
    order_detail_view = views.OrderDetailView

    def get_urls(self):
        """
        Let's make SURE that they get the right view
        """
        urls = [
                 url(r'^(?P<number>[-\w]+)/$',
                     self.order_detail_view.as_view(), name='order-detail'),
                ]
        urls += super().get_urls()

        return self.post_process_urls(urls)

application = OrdersDashboardApplication()
