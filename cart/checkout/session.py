import logging
from django.core.urlresolvers import reverse
from oscar.apps.checkout import exceptions, session
from . import forms, tax


logger = logging.getLogger('cart.checkout.session')


class CheckoutSessionMixin(session.CheckoutSessionMixin):
    """
    Implement tax and payment-related functionality specific to our site
    """

    def build_submission(self, **kwargs):
        """
        Pull together all of the order data for a submission
        """
        submission = super().build_submission(**kwargs)
        square_form = forms.SquareNonceForm(self.request.POST)

        #logger.info('submission dict before custom work: %s', submission)

        # If a shipping address is present, save it for the payment kwargs
        if submission['shipping_address'] and submission['shipping_method']:

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
        if 'user' in submission and hasattr(submission['user'], 'email'):
            email = submission['user'].email
        elif 'guest_email' in submission:
            email = submission['guest_email']
        else:
            email = False

        if email:
            submission['payment_kwargs']['email'] = email

        try:
            # Send along the card nonce retrieved in previous steps
            # TODO: Remove all the form crap once session methods are working
            nonce = self.get_card_nonce()

            if not nonce:
                if square_form.is_valid():
                    nonce = square_form.cleaned_data['nonce']
                else:
                    raise Exception('Cannot retrieve card nonce')

            submission['payment_kwargs']['nonce'] = nonce
        except:
            submission['payment_kwargs']['nonce'] = ''

        #logger.info('submission dict after custom work: %s', submission)

        # Return the submission data
        return submission


    def check_payment_data_is_captured(self, request):
        """
        Validate that we have a card nonce stored from Square
        """

        if not self.get_card_nonce():

            square_form = forms.SquareNonceForm(request.POST)

            if square_form.is_valid():
                self.save_card_nonce(square_form.cleaned_data['nonce'])

            else:
                msg = "We're sorry, we could not contact the payment gateway."
                raise exceptions.FailedPreCondition(
                        url=reverse('checkout:payment-details'),
                        message=msg)

        # Run parent function; currently doesn't do anything, but may be
        # implemented in the future
        super().check_payment_data_is_captured(request)


    def get_context_data(self, **kwargs):
        """
        Send the templates a flag to show tax separately
        """
        ctx = super().get_context_data()
        ctx['show_tax_separately'] = True
        return ctx

