from decimal import Decimal as D
from django.conf import settings
from django.contrib import messages
from django.views.generic import TemplateView
from duxdekes.exceptions import ChargeAdjustmentException, ChargeCaptureException
from oscar.apps.dashboard.orders.views import OrderDetailView as OscarOrderDetailView
from oscar.apps.order.exceptions import InvalidShippingEvent, InvalidPaymentEvent
from oscar.core.loading import get_class, get_model
from .forms import DiscountOrderForm, FinalizeOrderForm
from .util import get_orders, get_order_statistics, CURRENCY_HEADINGS, \
    REPORT_HEADINGS, AVG_SHIPPING_PER_ITEM

EventHandler = get_class('order.processing', 'EventHandler')
PaymentEventType = get_model('order', 'PaymentEventType')
ShippingEventType = get_model('order', 'ShippingEventType')


class OrderDetailView(OscarOrderDetailView):
    """
    Add a finalize order method to the OrderDetailView
    """
    order_actions = OscarOrderDetailView.order_actions + ('discount_order',
                                                          'finalize_order',)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Forms
        ctx['discount_order_form'] = self.get_discount_order_form()
        ctx['finalize_order_form'] = self.get_finalize_order_form()

        return ctx

    def get_discount_order_form(self):
        """
        Get an instance of the "discount order" form
        """
        kwargs = {}

        if self.object and self.object.final_basket_total:
            kwargs['initial'] = {
                'final_basket_total': self.object.final_basket_total,
            }

        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST

        return DiscountOrderForm(**kwargs)

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

    def discount_order(self, request, order):
        """
        Discount an order's basket total by changing the total used
        """
        handler = EventHandler()
        discount_form = self.get_discount_order_form()

        if discount_form.is_valid():
            try:
                # Save the final basket total in the order object
                discount_event_type, _ = PaymentEventType.objects.get_or_create(
                    code='discount', defaults={'name': 'Discount Set'})
                order.final_basket_total = \
                    discount_form.cleaned_data['final_basket_total']
                amount = order.shipping_incl_tax + order.final_basket_charge
                handler.handle_payment_event(order, discount_event_type, amount)
                order.save()

                messages.success(request, 'Discount applied successfully')

            except Exception as e:
                messages.error(request, '[Discount] ' + str(e))
        else:
            messages.error(request, "[Discount] The discount amount you've typed in is not valid")

        return self.reload_page()

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
                amount = D(order.final_shipping) + order.final_basket_charge

                # Capture the payment, with the NEW and IMPROVED amount
                if order.status == 'Pending':

                    # Adjust the total to reflect differences in the shipping costs
                    if amount != order.total_incl_tax:
                        adjust_event_type, _ = PaymentEventType.objects.get_or_create(
                            code='adjust', defaults={'name': 'Adjusted'})
                        handler.handle_payment_event(order, adjust_event_type, amount)
                        handler.handle_order_status_change(order, 'Order Total Adjusted',
                                note_msg='Shipping/order total adjusted')

                        order.save()

                    capture_event_type, _ = PaymentEventType.objects.get_or_create(
                        code='capture', defaults={'name': 'Captured'})
                    handler.handle_payment_event(order, capture_event_type, amount)
                    handler.handle_order_status_change(order, 'Charge Finalized',
                            note_msg='Customer successfully charged')

                # Set everything as shipped, and calculate the lines if needed
                lines = [line for line in order.lines.all()]
                line_quantities = [line.quantity for line in order.lines.all()]
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
                messages.error(request, '[Payment] ' + str(e))
            except InvalidShippingEvent as e:
                msg = """
                [Shipping] There was a problem registering the shipping event. This was
                unexpected, but shouldn't actually affect anything.
                """
                messages.error(request, msg)

        else:
            messages.error(request, "[Form] The final amount you've typed in is not valid")

        return self.reload_page()


class ShippingHistoryReport(TemplateView):
    """
    Display an order history
    """
    template_name = 'dashboard/orders/shipping_report.html'

    def get_context_data(self, **kwargs):
        """
        Add report data to the context dictionary

        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)

        orders = []
        total_avg_shipping = D(0)
        num_avg_shipping = 0
        aggregate_average = D(0)

        for order in get_orders():

            statistics = get_order_statistics(order)

            avg_shipping_per_item = statistics.get(AVG_SHIPPING_PER_ITEM)

            if avg_shipping_per_item is not None and avg_shipping_per_item > 0:
                total_avg_shipping += avg_shipping_per_item
                num_avg_shipping += 1

            orders.append(statistics)

        # Calculate the averages
        if num_avg_shipping > 0:
            aggregate_average = total_avg_shipping / num_avg_shipping

        # Attach report information
        context.update({
            'currency_headings': CURRENCY_HEADINGS,
            'default_currency': settings.OSCAR_DEFAULT_CURRENCY,
            'report_headings': REPORT_HEADINGS,
            'aggregate_average': aggregate_average,
            'orders': orders
        })

        return context
