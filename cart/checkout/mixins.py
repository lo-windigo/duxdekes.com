from django.conf import settings
from oscar.apps.checkout import mixins
from oscar.apps.payment.models import SourceType, Source
from oscar.apps.payment.exceptions import PaymentError, UnableToTakePayment
import squareconnect
from squareconnect.rest import ApiException
from squareconnect.apis.transactions_api import TransactionsApi
from duxdekes.models import SquareSettings


class OrderPlacementMixin(mixins.OrderPlacementMixin):
    """
    Mixin which provides functionality for paying with SquareSpace
    """

    def handle_payment(self, order_number, total, **kwargs):
        """
        Try to process the payment using the Square REST API
        """
        square_settings = SquareSettings.get_settings()
        squareconnect.configuration.access_token = \
            square_settings.access_token
        source_type, __ = SourceType.objects.get_or_create(name='Square')
        api_instance = TransactionsApi()
        nonce = kwargs.get('nonce', False)

        if not nonce:
            raise PaymentError('No card nonce provided')

        # Debugging - allow for testing without pinging the Square API
        elif settings.DEBUG and nonce == 'TEST':
            source = Source(source_type=source_type,
                            amount_debited=total.incl_tax,
                            reference='Test entry')

            self.add_payment_source(source)
            self.add_payment_event('auth', total.incl_tax)

            return

        # Set the total amount to charge, in US Cents
        amount = {
            'amount': int(100*float(total.incl_tax)),
            'currency': 'USD'
        }

        # TODO: Pass billing address, email to provide square chargeback
        # protection
        body = {
            'idempotency_key': str(order_number),
            'card_nonce': nonce,
            'amount_money': amount,
            'delay_capture': True,
        }

        try:
            # Charge
            api_response = api_instance.charge(square_settings.location_id,
                    body, )

            # Save the response ID
            if not api_response.transaction:
                raise ApiException(', '.join(api_response.errors))

        except ApiException as e:
            if settings.DEBUG:
                print("Exception when calling TransactionApi->charge: {}".format(e))
            raise PaymentError(str(e))

        # Request was successful - record the "payment source".  As this
        # request was a 'pre-auth', we set the 'amount_allocated' - if we had
        # performed an 'auth' request, then we would set 'amount_debited'.
        source = Source(source_type=source_type,
                        amount_debited=total.incl_tax,
                        reference=api_response.transaction.reference_id)

        self.add_payment_source(source)

        # Also record payment event
        self.add_payment_event('auth', total.incl_tax)

