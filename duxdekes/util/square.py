import datetime, logging, sys, uuid
from duxdekes.models import SquareSettings
from duxdekes.exceptions import ChargeAdjustmentException, ChargeCaptureException
from square.client import Client
from square.exceptions.api_exception import APIException

logger = logging.getLogger('duxdekes.util.square')
square_settings = SquareSettings.get_settings()
sandboxed = None


def get_client():
    """
    Get an instance of the Square Client, set up the access token and
    environment
    """
    if currently_sandboxed():
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
    client = get_client()

    try:
        # Create the request body, which specifies version token
        payment = get_previous_payment(reference)
        body = { 'version_token': payment['payment']['version_token'], }

        # Capture the previously authorized transaction
        api_response = client.payments.complete_payment(reference, body)

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


def adjust_charge(reference, new_amount):
    """
    Refund the difference between the final capture and the actual cost
    """
    client = get_client()

    try:
        body = {
                'idempotency_key': generate_idempotency_key(),
                'payment': {
                    'amount_money': build_amount_payload(new_amount)
                    }
                }

        update_response = client.payments.update_payment(reference, body)

        if update_response.is_error():
            errors = ', '.join([err.detail for err in update_response.errors])
            raise APIException(errors)

        return update_response.body['payment']

    except APIException as e:
        msg = "Problem adjusting the authorized cost to {}: {}"\
                .format(new_amount, e)
        logger.error(msg, exc_info=sys.exc_info())
        raise ChargeAdjustmentException(msg) from e


def get_previous_payment(payment_id):
    client = get_client()
    payment_response = client.payments.get_payment(payment_id)

    if payment_response.is_error():
        errors = ', '.join([err.detail for err in payment_response.errors])
        raise APIException(errors)

    return payment_response.body


def build_amount_payload(dollar_amount):
    return {
        'amount': int(100*float(dollar_amount)),
        'currency': 'USD'
    }


def generate_idempotency_key():
    return str(uuid.uuid4())

def currently_sandboxed():
    if sandboxed === None:
        sandboxed = square_settings.application_id[:7] == 'sandbox'
    return sandboxed
