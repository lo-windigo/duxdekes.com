from django.core.urlresolvers import reverse
from oscar.apps.checkout import exceptions, session
from . import tax


class CheckoutSessionMixin(session.CheckoutSessionMixin):
    """
    Implement tax and payment-related functionality specific to our site
    """

    def build_submission(self, **kwargs):
        submission = super().build_submission(**kwargs)

        # If a shipping address is present, save it for the payment kwargs
        if hasattr(submission, 'shipping_address') and hasattr(submission,
                'shipping_method'):

            # Copy the shipping address object to the payment kwargs to provide
            # to Square (provides chargeback protection)
            submission['payment_kwargs']['shipping_address'] = submission['shipping_address']

            # Apply taxes to the basket
            tax.apply_to(submission)

            # Recalculate order total to ensure we have a tax-inclusive total
            submission['order_total'] = self.get_order_totals(
                submission['basket'],
                shipping_charge=submission['shipping_charge'])

        # Add user email to payment kwargs formation for Square chargeback protection
        # ( billing_address is already sent into the payment kwargs )
        if hasattr(submission, 'user') and hasattr(submission['user'], email):
            email = submission['user'].email
        elif hasattr(submission, 'guest_email'):
            email = submission['guest_email']
        else:
            email = False

        if email:
            submission['payment_kwargs']['email'] = email

        # Send along the card nonce retrieved in previous steps
        submission['payment_kwargs']['nonce'] = self.get_card_nonce()

        # Return the submission data
        return submission


    def check_payment_data_is_captured(self, request):
        """
        Validate that we have a card nonce stored from Square
        """

        if not self.get_card_nonce():
            msg = "We're sorry, we could not contact the payment gateway."
            raise exceptions.FailedPreCondition(
                    url=reverse('checkout:payment-details'),
                    message=msg)

        # Run parent function; currently doesn't do anything, but may be
        # implemented in the future
        super().check_payment_data_is_captured(request)

