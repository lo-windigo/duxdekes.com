from duxdekes.util.square import adjust_charge, capture_payment
from oscar.apps.order import exceptions
from oscar.apps.order.exceptions import InvalidPaymentEvent
from oscar.apps.order.processing import EventHandler as OscarEventHandler


class EventHandler(OscarEventHandler):
    """
    Override Oscar's default event handling class to provide our custom workflow
    """

    def handle_payment_event(self, order, event_type, amount, lines=None,
            line_quantities=None, **kwargs):
        """
        Integrate some Square-specific payment details
        """

        # Validate that we have valid amounts
        if order.total_incl_tax < amount:
            msg = 'The authorized cost cannot be less than the final cost'
            raise InvalidPaymentEvent(msg)

        # Finalize a previously authorized order
        if event_type.code == 'capture':
            try:
                # Get the old transaction ID
                auth_payment_event = order.payment_events.filter(
                        event_type__code='auth').latest('date_created')
                auth_payment_reference = auth_payment_event.reference
                capture_payment(auth_payment_reference)
                kwargs['reference'] = auth_payment_reference
            except Exception as e:
                msg = 'Could not get the authorization payment event'
                raise InvalidPaymentEvent(msg) from e

        # Adjust the cost of an order
        elif event_type.code == 'adjust': 
            try:
                # Get the old transaction ID
                cap_payment_event = order.payment_events.filter(
                        event_type__code='capture').latest('date_created')
                cap_payment_reference = cap_payment_event.reference
            except Exception as e:
                msg = 'Could not get the capture payment event'
                raise InvalidPaymentEvent(msg) from e

            try:
                kwargs['reference'] = adjust_charge(order.number,
                        cap_payment_reference, order.total_incl_tax, amount)
            except Exception as e:
                msg = 'Unable to adjust the charge'
                raise InvalidPaymentEvent(msg) from e

        return super().handle_payment_event(order, event_type, amount, lines,
                line_quantities, **kwargs)

