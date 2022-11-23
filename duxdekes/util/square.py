import datetime, logging, sys
from duxdekes.models import SquareSettings
from duxdekes.exceptions import ChargeAdjustmentException, ChargeCaptureException
from square.client import Client
from pprint import pprint

logger = logging.getLogger('duxdekes.util.square')
square_settings = SquareSettings.get_settings()


def get_client():
    """
    Get an instance of the Square Client, set up the access token and
    environment
    """
    if square_settings.application_id[:7] == 'sandbox':
        environment = 'sandbox'
    else:
        environment = 'production'

    return Client(access_token=square_settings.access_token,
            environment=environment, square_version='2022-11-16')

def get_location():
    """
    Return the current location ID
    """
    return square_settings.location_id


def capture_payment(reference):
    """
    Capture a payment authorized previously
    """
    client = self.get_client()

    try:
        # Capture the previously authorized transaction
        api_response = client.payments.complete_payment(reference)

        # Something went wrong with the API; time to deal with it
        if api_response.is_error():

            errors = ', '.join([err.detail for err in api_response.errors])

            raise Exception(errors)

        # No success value, code or anything
        return

    except Exception as e:
        msg = "Problem finalizing the transaction"
        logger.error(msg, exc_info=sys.exc_info())
        raise ChargeCaptureException(msg) from e


def adjust_charge(order_number, reference, new_amount):
    """
    Refund the difference between the final capture and the actual cost
    """
    client = self.get_client()

    # Fetch payment details from Square
    try:
        payment_response = client.get_payment(reference)

        if payment_response.is_error():
            errors = ', '.join([err.detail for err in payment_response.errors])
            raise ApiException(errors)

        payment = payment_response.body

    except ApiException as e:
        msg = "Problem retrieving the previous paymnet: {}"\
                .format(e)
        logger.error(msg, exc_info=sys.exc_info())
        raise ChargeAdjustmentException(msg) from e

    try:
        payment['idempotency_key'] = generate_idempotency_key()
        payment['amount_money'] = build_amount_payload(new_amount)

        update_response = client.update_payment(reference, payment)

        if update_response.is_error():
            errors = ', '.join([err.detail for err in update_response.errors])
            raise ApiException(errors)

    except ApiException as e:
        msg = "Problem adjusting the authorized cost by {}: {}"\
                .format(refund_amount, e)
        logger.error(msg, exc_info=sys.exc_info())
        raise ChargeAdjustmentException(msg) from e


def build_amount_payload(dollar_amount):
    return {
        'amount': int(100*float(dollar_amount)),
        'currency': 'USD'
    }
    

def generate_idempotency_key():
    return str(uuid.uuid4())

