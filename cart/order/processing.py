from duxdekes.util.square import adjust_charge, capture_payment
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
        Integrate some Square-specific payment details
        """

        # Finalize a previously authorized order
        if event_type == 'capture':
            try:
                if order.total_incl_tax < amount:
                    error = """
                    The original authorized cost is less than the cost with shipping
                    """
                    raise ChargeCaptureException(error)

                # Get the old transaction ID
                auth_payment_event = order.payment_events.get(event_type__code='auth')
                auth_payment_reference = auth_payment_event.reference
                kwargs['reference'] = capture_payment(auth_payment_reference)
            except Exception as e:
                msg = 'Could not get the authorization payment event'
                raise InvalidPaymentEvent(msg) from e

        # Adjust the cost of an order
        elif event_type == 'adjust': 
            try:
                # Get the old transaction ID
                cap_payment_event = order.payment_events.get(event_type__code='capture')
                cap_payment_reference = cap_payment_event.reference
                kwargs['reference'] = adjust_charge(order.id,
                        cap_payment_reference, order.total_incl_tax, amount)
            except Exception as e:
                msg = 'Could not get the capture payment event'
                raise InvalidPaymentEvent(msg) from e


        return super().handle_payment_event(order, event_type, amount, lines,
                line_quantities, **kwargs)

