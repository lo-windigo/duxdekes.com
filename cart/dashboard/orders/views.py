from django.contrib import messages
from oscar.apps.dashboard.orders.views import OrderDetailView as OscarOrderDetailView
from oscar.core.loading import get_class
from .forms import FinalizeOrderForm


EventHandler = get_class('order.processing', 'EventHandler')


class OrderDetailView(OscarOrderDetailView):
    """
    Add a finalize order method to the OrderDetailView
    """
    order_actions = OscarOrderDetailView.order_actions + ('finalize_order',)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Forms
        ctx['finalize_order_form'] = self.get_finalize_order_form()

        return ctx

    def get_finalize_order_form(self):
        """
        Get an instance of the "finalize order" form
        """
        kwargs = {
            'data': None
        }
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return FinalizeOrderForm(**kwargs)

    def finalize_order(self, request, order):
        """
        Take a previously authorized order, and finalize the charge
        """
        handler = EventHandler()
        finalize_form = self.get_finalize_order_form()

        if finalize_form.is_valid():

            try:
                # Capture the payment, with the NEW and IMPROVED amount
                amount = D(finalize_form.cleaned_data.final_shipping) +
                    order.basket_total_incl_tax
                handler.handle_payment_event(order, 'capture', amount)

                # Set everything as shipped, and calculate the lines if needed
                lines = [ line for line in order.lines.all() ]
                line_quantities = [ line.quantity for line in order.lines.all() ]
                handler.handle_shipping_event(order, 'shipped', lines, line_quantities)

                messages.success(request, "Order successfully charged.")
            except InvalidPaymentEvent as e:
                msg = """
                [Payment] There was a problem finalizing the payment: the payment gateway
                may be experiencing problems.

                Please try again in a few minutes.
                """
                messages.error(request, msg)
            except InvalidShippingEvent as e:
                msg = """
                [Shipping] There was a problem registering the shipping event. This was
                unexpected, but shouldn't actually affect anything.
                """
                messages.error(request, msg)

        else:
            messages.error(request, "[Form] The final amount you've typed in is not valid")


