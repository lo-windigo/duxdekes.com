from django.core.urlresolvers import reverse
from oscar.apps.checkout import exceptions, session
from . import tax


class CheckoutSessionMixin(session.CheckoutSessionMixin):
    """
    Implement tax and payment-related functionality specific to our site
    """

    def build_submission(self, **kwargs):
        submission = super(CheckoutSessionMixin, self).build_submission(
            **kwargs)

        if submission['shipping_address'] and submission['shipping_method']:
            tax.apply_to(submission)

            # Recalculate order total to ensure we have a tax-inclusive total
            submission['order_total'] = self.get_order_totals(
                submission['basket'],
                shipping_charge=submission['shipping_charge'])

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

