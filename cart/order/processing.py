from duxdekes.util.square import finalize_payment
from oscar.apps.order import exceptions
from oscar.core.loading import get_model, get_class
from oscar.apps.order.exceptions import InvalidPaymentEvent
from oscar.apps.order.processing import EventHandler as OscarEventHandler

PaymentEventType = get_model('order', 'PaymentEventType')

class EventHandler(OscarEventHandler):
    """
    Override Oscar's default event handling class to provide our custom workflow
    """

    def handle_payment_event(self, order, event_type, amount, lines=None,
            line_quantities=None, **kwargs):
        """
        Finalize a previously authorized order
        """
        event_type, __ = PaymentEventType.objects.get_or_create(
                name='capture')

        # Get the old transaction ID
        try:
            auth_payment_event = order.payment_events.get(event_type__code='auth')
            auth_payment_reference = auth_payment_event.reference
        except:
            raise exceptions.InvalidPaymentEvent(
                'Could not get the original payment authorization event')

        finalize_payment(order.id, auth_payment_reference, order.total_incl_tax, amount)

        return super().handle_payment_event(order, event_type, amount, lines,
                line_quantities, reference=auth_payment_reference, **kwargs)

