from decimal import Decimal as D
from django.contrib import messages
from duxdekes.exceptions import ChargeAdjustmentException, ChargeCaptureException
from oscar.apps.dashboard.orders.views import OrderDetailView as OscarOrderDetailView
from oscar.apps.order.exceptions import InvalidShippingEvent, InvalidPaymentEvent
from oscar.core.loading import get_class, get_model
from .forms import FinalizeOrderForm


EventHandler = get_class('order.processing', 'EventHandler')
PaymentEventType = get_model('order', 'PaymentEventType')
ShippingEventType = get_model('order', 'ShippingEventType')


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
        kwargs = {}

        if self.object and self.object.final_shipping:
            kwargs['initial'] = {
                'final_shipping': self.object.final_shipping,
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
                # Save the final shipping value, just in case something gets
                # ruined
                order.final_shipping = finalize_form.cleaned_data['final_shipping']
                order.save()

                # Calculate the new final amount
                amount = D(order.final_shipping) + order.basket_total_incl_tax

                # Capture the payment, with the NEW and IMPROVED amount
                if order.status == 'Pending':
                    capture_event_type, _ = PaymentEventType.objects.get_or_create(
                            code='capture', defaults={'name': 'Captured'})
                    handler.handle_payment_event(order, capture_event_type, order.total_incl_tax)
                    handler.handle_order_status_change(order, 'Needs Adjustment',
                            note_msg='Customer successfully charged')
                    # Maybe this will allow us to see the capture event?
                    order.save()

                # Adjust the total with a refund to the customer to reflect
                # differences in the shipping costs
                if order.status == 'Needs Adjustment' and amount != order.total_incl_tax:
                    adjust_event_type, _ = PaymentEventType.objects.get_or_create(
                            code='adjust', defaults={'name': 'Adjusted'})
                    handler.handle_payment_event(order, adjust_event_type, amount)

                    # Do we really need this order status change?
                    #handler.handle_order_status_change(order, 'Adjusted',
                    #        note_msg='Customer refunded difference in shipping')

                # Set everything as shipped, and calculate the lines if needed
                lines = [ line for line in order.lines.all() ]
                line_quantities = [ line.quantity for line in order.lines.all() ]
                shipping_event_type, _ = ShippingEventType.objects.get_or_create(
                        code='shipped', defaults={'name': 'Shipped'})

                handler.handle_shipping_event(order, shipping_event_type,
                        lines, line_quantities)
                handler.handle_order_status_change(order, 'Processed',
                        note_msg='Customer successfully charged')

            except ChargeAdjustmentException as e:
                msg = """
                There was a problem adjusting the final charge to
                reflect the real shipping charge.
                """

                messages.error(request, msg + str(e))
                handler.handle_order_status_change(order, 'Needs Adjustment',
                        note_msg=msg)
            except ChargeCaptureException as e:
                msg = """
                There was a problem finalizing the payment: the payment gateway
                may be experiencing problems.

                Please try again in a few minutes.
                """
                messages.error(request, msg)
            except InvalidPaymentEvent as e:
                messages.error(request, '[Payment] '+str(e))
            except InvalidShippingEvent as e:
                msg = """
                [Shipping] There was a problem registering the shipping event. This was
                unexpected, but shouldn't actually affect anything.
                """
                messages.error(request, msg)

        else:
            messages.error(request, "[Form] The final amount you've typed in is not valid")

        return self.reload_page()

