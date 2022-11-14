import datetime
from django.conf import settings
import logging
from oscar.apps.checkout import mixins
from oscar.apps.payment.models import SourceType, Source
from oscar.apps.payment.exceptions import PaymentError, UnableToTakePayment
from oscar.core.loading import get_class
from square import client
from square.rest import ApiException
from duxdekes.models import SquareSettings


logger = logging.getLogger('cart.checkout.mixins')


class OrderPlacementMixin(mixins.OrderPlacementMixin):
    """
    Mixin which provides functionality for paying with SquareSpace
    """

    def handle_payment(self, order_number, total, **kwargs):
        """
        Try to process the payment using the Square REST API
        """
        square_settings = SquareSettings.get_settings()
        squareClient = client.Client({"access_token": square_settings.access_token})
            
        source_type, __ = SourceType.objects.get_or_create(name='Square')
        source = Source(source_type=source_type,
                        amount_allocated=total.incl_tax)
        token = getattr(kwargs, 'token', self.get_card_token())
        today = datetime.date.today()

        if not token:
            raise PaymentError('No payment token provided')

        # Debugging - allow for testing without pinging the Square API
        elif settings.DEBUG and token == 'TEST':
            self.add_payment_source(source)
            self.add_payment_event('auth', total.incl_tax, reference='Test entry')
            return

        # Set the total amount to charge, in US Cents
        amount = {
            'amount': int(100*float(total.incl_tax)),
            'currency': 'USD'
        }

        # Start the request for authorization, including shipping address and
        # user email (if provided)
        body = {
            'idempotency_key': "{}_{}_auth".format(
                today.strftime('%Y%m%d'),
                order_number),
            'source_id': token,
            'amount_money': amount,
            'autocomplete': False,
        }

        # Add user information for chargeback protection
        if 'email' in kwargs:
            body['buyer_email_address'] = kwargs['email']

        for addr_type in 'shipping_address', 'billing_address':
            if addr_type in kwargs:
                addr_object = kwargs[addr_type]
                address = dict()

                address['address_line_1'] = addr_object.line1
                address['address_line_2'] = addr_object.line2
                address['address_line_3'] = addr_object.line3
                address['locality'] = addr_object.line4
                address['administrative_district_level_1'] = addr_object.state
                address['postal_code'] = addr_object.postcode
                address['country'] = addr_object.country.iso_3166_1_a2
                address['first_name'] = addr_object.first_name
                address['last_name'] = addr_object.last_name

                body[addr_type] = address

        try:
            # Charge
            # TODO: Check method signature
            api_response = squareClient.payments.create_payment(square_settings.location_id, body)

            # Save the response ID
            if not api_response.transaction:
                raise ApiException(', '.join(api_response.errors))

        except ApiException as e:
            msg = "Exception when calling TransactionApi->charge: {}".format(e)
            logger.info(msg)
            raise PaymentError(msg) from ApiException

        # Request was successful - record the "payment source".  As this
        # request was a 'pre-auth', we set the 'amount_allocated' - if we had
        # performed an 'auth' request, then we would set 'amount_debited'.
        self.add_payment_source(source)

        # Also record payment event
        self.add_payment_event('auth', total.incl_tax, reference=api_response.transaction.id)


    def get_card_token(self):
        """
        Get the card payment token, and return an empty string if unset
        """
        return self.checkout_session._get('payment', 'token', '')


    def save_card_token(self, token):
        """
        Save the credit card payment token value to the session
        """
        self.checkout_session._set('payment', 'token', token)

