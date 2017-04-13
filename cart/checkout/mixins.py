from django.conf import settings
from oscar.apps.checkout import mixins
from oscar.apps.payment.models import SourceType, Source
from oscar.apps.payment.exceptions import UnableToTakePayment
from squareconnect.rest import ApiException
from squareconnect.apis.transaction_api import TransactionApi


class OrderPlacementMixin(mixins.CheckoutSessionMixin):
    """
    Mixin which provides functionality for paying with SquareSpace
    """

    def handle_payment(self, order_number, total, **kwargs):
        """
        Try to process the payment using the Square REST API
        """

	api_instance = TransactionApi()

        # Set the total amount to charge, in US Cents
        amount = {
            'amount': 100*total.incl_tax,
            'currency': 'USD'
        }
        body = {
            'idempotency_key': order_number,
            'card_nonce': kwargs['nonce'],
            'amount_money': amount
        }

        try:
            # Charge
            api_response = api_instance.charge(settings.SQUARE_ACCESS_TOKEN,
                    settings.SQUARE_LOCATION_ID,
                    body)
            res = api_response.transaction
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

