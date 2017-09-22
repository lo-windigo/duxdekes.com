from django.conf import settings
from oscar.apps.checkout import mixins
from oscar.apps.payment.models import SourceType, Source
from oscar.apps.payment.exceptions import UnableToTakePayment
import squareconnect
from squareconnect.rest import ApiException
from squareconnect.apis.transactions_api import TransactionsApi
from . import models


class OrderPlacementMixin(mixins.OrderPlacementMixin):
    """
    Mixin which provides functionality for paying with SquareSpace
    """

    def handle_payment(self, order_number, total, **kwargs):
        """
        Try to process the payment using the Square REST API
        """
        square_settings = models.SquareSettings.get_settings()
        squareconnect.configuration.access_token = \
            square_settings.access_token
        api_instance = TransactionApi()

        # Set the total amount to charge, in US Cents
        amount = {
            'amount': int(100*float(total.incl_tax)),
            'currency': 'USD'
        }

        try:
            body = {
                'idempotency_key': str(order_number),
                'card_nonce': kwargs['nonce'],
                'amount_money': amount
            }
        except:
            # TODO: better error, get the type of ValueException perhaps
            print('Problem getting the card nonce value!')

        try:
            # Charge
            api_response = api_instance.charge(square_settings.location_id, body)

            # Save the response ID
            if api_response.transaction:
                res = api_response.transaction.reference_id

            else:
                raise ApiException(', '.join(api_response.errors))

        except ApiException as e:
            if settings.DEBUG:
                print("Exception when calling TransactionApi->charge: {}".format(e))
            raise UnableToTakePayment(str(e))

        # Request was successful - record the "payment source".  As this
        # request was a 'pre-auth', we set the 'amount_allocated' - if we had
        # performed an 'auth' request, then we would set 'amount_debited'.
        source_type, _ = SourceType.objects.get_or_create(name='Square')
        source = Source(source_type=source_type,
                        amount_debited=total.incl_tax,
                        reference=res)

        self.add_payment_source(source)

        # Also record payment event
        self.add_payment_event('auth', total.incl_tax)

