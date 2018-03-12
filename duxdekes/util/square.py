from duxdekes.models import SquareSettings
from duxdekes.exceptions import ChargeAdjustmentException, ChargeCaptureException
import squareconnect
from squareconnect.rest import ApiException
from squareconnect.apis.transactions_api import TransactionsApi


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
        if hasattr(api_response, 'errors'):
            if api_response.errors:
                errors = ', '.join([err.detail for err in api_response.errors])
                exception = ApiException(errors)
            else:
                exception = ApiException()

            raise exception

        # Return the transaction id
        return api_response.transaction.id

    except Exception as e:
        raise ChargeCaptureException("Problem finalizing the transaction") from e


def adjust_charge(order_number, reference, original_amount, new_amount):
    """
    Refund the difference between the final capture and the actual cost
    """
    square_settings = SquareSettings.get_settings()
    api_instance = get_api(square_settings.access_token)
    refund_amount = float(original_amount - new_amount)
    refund_in_cents = int(100*refund_amount)

    # Get the previous captured transactions' tender id
    try:
        api_response = api_instance.retrieve_transaction(
                square_settings.location_id,
                reference)

        if hasattr(api_response, 'errors'):
            if api_response.errors:
                errors = ', '.join([err.detail for err in api_response.errors])
                exception = ApiException(errors)
            else:
                exception = ApiException()

            raise exception

        previous_tender = api_response.transaction.tenders[0].id

    except ApiException as e:
        msg = "Problem retrieving the previous auth transaction"
        raise ChargeCaptureException(msg) from e
    except IndexError as e:
        raise ChargeCaptureException('Problem retrieving the tender id') from e

    amount = {
        'amount': refund_in_cents,
        'currency': 'USD'
    }

    body = {
        'idempotency_key': "{}_adjust".format(order_number),
        'tender_id': previous_tender,
        'amount_money': amount,
        'reason': 'Adjustment in shipping costs',
    }

    try:
        api_response = api_instance.create_refund(square_settings.location_id,
            body)
    except ApiException as e:
        msg = "Problem adjusting the authorized cost by {}: {}"\
                .format(refund_amount, e)
        raise ChargeAdjustmentException(msg) from e

