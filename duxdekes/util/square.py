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


def finalize_payment(order_number, reference, original_amount, new_amount):
    """
    Capture a payment authorized previously, and refund the difference
    """
    square_settings = SquareSettings.get_settings()
    api_instance = get_api(square_settings.access_token)

    if original_amount < new_amount:
        error = """
        The original authorized cost is less than the cost with shipping
        """
        raise ChargeCaptureException(error)

    try:
        # Capture the previously authorized transaction
        api_response = api_instance.capture_transaction(
                square_settings.location_id,
                reference)

        # Save the response ID
        if not api_response.transaction:
            raise ApiException(', '.join(api_response.errors))

    except ApiException as e:
        msg = "Problem finalizing the transaction: " + str(e)
        raise ChargeCaptureException(msg) from ApiException

    charge_id = api_response.transaction.id

    # If we estimated the price perfectly, and do not have to refund the
    # difference break out
    if original_amount == new_amount:
        return

    # Refund the customer for the difference in auth'd amount
    refund_amount = float(original_amount - new_amount)
    refund_in_cents = int(100*refund_amount)

    # Get the previous captured transactions' tender idtender id
    try:
        api_response = api_instance.retrieve_transaction(
                square_settings.location_id,
                reference)

        if not api_response.transaction:
            raise ApiException(', '.join(api_response.errors))

        previous_tender = api_response.transaction.tenders[0].id

    except ApiException as e:
        msg = "Problem retrieving the previous auth transaction: " + str(e)
        raise ChargeCaptureException(msg) from ApiException
    except IndexError:
        raise ChargeCaptureException('Problem retrieving the tender id')

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
        raise ChargeAdjustmentException(msg) from ApiException

