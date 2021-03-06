import datetime, logging, sys
from duxdekes.models import SquareSettings
from duxdekes.exceptions import ChargeAdjustmentException, ChargeCaptureException
import squareconnect
from squareconnect.rest import ApiException
from squareconnect.apis.transactions_api import TransactionsApi
from pprint import pprint

logger = logging.getLogger('duxdekes.util.square')


def get_api(token):
    """
    Get an instance of the Square API, set up the access token
    """
    squareconnect.configuration.access_token = token
    return TransactionsApi()


def capture_payment(reference):
    """
    Capture a payment authorized previously
    """
    square_settings = SquareSettings.get_settings()
    api_instance = get_api(square_settings.access_token)

    try:
        # Capture the previously authorized transaction
        api_response = api_instance.capture_transaction(
                square_settings.location_id,
                reference)

        # Something went wrong with the API; time to deal with it
        if api_response.errors:

            errors = ', '.join([err.detail for err in api_response.errors])

            raise ApiException(errors)

        # No success value, code or anything
        return

    except Exception as e:
        msg = "Problem finalizing the transaction"
        logger.error(msg, exc_info=sys.exc_info())
        raise ChargeCaptureException(msg) from e


def adjust_charge(order_number, reference, original_amount, new_amount):
    """
    Refund the difference between the final capture and the actual cost
    """
    square_settings = SquareSettings.get_settings()
    api_instance = get_api(square_settings.access_token)
    refund_amount = float(original_amount - new_amount)
    refund_in_cents = int(100*refund_amount)
    today = datetime.date.today()

    # Get the previous captured transactions' tender id
    try:
        api_response = api_instance.retrieve_transaction(
                square_settings.location_id,
                reference)

        if api_response.errors is not None:
            errors = ', '.join([err.detail for err in api_response.errors])
            raise ApiException(errors)

        previous_tender = api_response.transaction.tenders[0].id

    except ApiException as e:
        msg = "Problem retrieving the previous auth transaction"
        logger.error(msg, exc_info=sys.exc_info())
        raise ChargeCaptureException(msg) from e
    except IndexError as e:
        msg = 'Problem retrieving the tender id'
        logger.error(msg, exc_info=sys.exc_info())
        raise ChargeCaptureException(msg) from e

    amount = {
        'amount': refund_in_cents,
        'currency': 'USD'
    }

    body = {
        'idempotency_key': "{}_{}_adjust".format(
            today.strftime('%Y%m%d'),
            order_number),
        'tender_id': previous_tender,
        'amount_money': amount,
        'reason': 'Adjustment in shipping costs',
    }

    try:
        api_response = api_instance.create_refund(square_settings.location_id,
            reference, body)

        return api_response.refund.transaction_id

    except ApiException as e:
        msg = "Problem adjusting the authorized cost by {}: {}"\
                .format(refund_amount, e)
        logger.error(msg, exc_info=sys.exc_info())
        raise ChargeAdjustmentException(msg) from e

